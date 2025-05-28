import os

import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import boto3

from utils.user_manager import update_background_url
from dotenv import load_dotenv

load_dotenv()  # .env 파일을 읽어서 환경변수로 등록함

aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
        )
        print("S3 bucket connected!")
        return s3
    except Exception as e:
        print("S3 connection error:", e)
        return None

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
COMPRESS_LIMIT = 3 * 1024 * 1024  # 압축 대상: 1MB ~ 3MB

def compress_image(image, max_size=MAX_FILE_SIZE, quality_start=85):
    """JPEG 품질을 낮춰서 max_size 이하로 줄임"""
    buffer = BytesIO()
    quality = quality_start
    while quality >= 10:
        buffer.seek(0)
        buffer.truncate()
        image.save(buffer, format="JPEG", quality=quality)
        if buffer.tell() <= max_size:
            buffer.seek(0)
            return buffer
        quality -= 5
    return None

def upload_image_from_url(s3, url, bucket, s3_key, user_id):
    try:
        response = requests.get(url)
        response.raise_for_status()

        content = response.content
        file_size = len(content)

        image = Image.open(BytesIO(content))
        image.verify()  # 유효성 검사
        image = Image.open(BytesIO(content))  # 다시 열기 (verify 후 이미지 객체 무효화됨)

        # 압축이 필요한 경우
        if MAX_FILE_SIZE < file_size <= COMPRESS_LIMIT:
            print(f"Compressing image ({file_size / 1024:.2f} KB)...")
            if image.mode != "RGB":
                image = image.convert("RGB")  # JPEG 압축을 위해 RGB로 변환

            buffer = compress_image(image)
            if buffer is None:
                print("Failed to compress image under 1MB.")
                return False
        elif file_size > COMPRESS_LIMIT:
            print(f"Image too large to upload: {file_size / 1024:.2f} KB")
            return False
        else:
            # 1MB 이하인 경우 그대로 업로드
            buffer = BytesIO(content)

        s3.upload_fileobj(
            Fileobj=buffer,
            Bucket=bucket,
            Key=s3_key,
            ExtraArgs={"ContentType": "image/jpeg", "ACL": "public-read"},
        )
        print("Upload successful!")
        try:
            update_background_url(user_id, s3_key)
            return True
        except:
            return False

    except Exception as e:
        print("Upload failed:", e)
        return False