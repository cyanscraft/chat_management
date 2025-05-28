import io

import requests
from PIL import Image, ImageDraw


def resize_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    img_w, img_h = img.size

    # 타겟 비율
    target_ratio = target_w / target_h
    # 원본 비율
    img_ratio = img_w / img_h

    # 확대할 크기 계산
    if img_ratio > target_ratio:
        # 원본이 더 넓으면 높이에 맞춰서 리사이즈 (너비가 타겟보다 커짐)
        new_h = target_h
        new_w = int(new_h * img_ratio)
    else:
        # 원본이 더 높거나 같으면 너비에 맞춰서 리사이즈 (높이가 타겟보다 커짐)
        new_w = target_w
        new_h = int(new_w / img_ratio)

    resized_img = img.resize((new_w, new_h), Image.LANCZOS)

    # 중앙 기준 crop
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h

    cropped_img = resized_img.crop((left, top, right, bottom))
    return cropped_img



def load_image_from_url(url: str) -> Image.Image:
    response = requests.get(url)
    response.raise_for_status()  # 요청 실패 시 에러 발생

    img_bytes = io.BytesIO(response.content)
    img = Image.open(img_bytes).convert("RGBA")
    return img

def add_rounded_corners(im: Image.Image, radius: int) -> Image.Image:
    # im은 RGBA 이미지여야 함
    circle = Image.new('L', (radius * 2, radius * 2), 0)  # 흰색 원 마스크 만들기
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', im.size, 255)  # 기본 알파(불투명) 마스크
    w, h = im.size

    # 각 모서리에 원 마스크 붙이기 (검은 부분은 투명)
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))  # 왼쪽 위
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))  # 오른쪽 위
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))  # 왼쪽 아래
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))  # 오른쪽 아래

    im.putalpha(alpha)
    return im

def draw_wrapped_text(draw, text, font, x, y, max_width, fill=(255, 255, 255, 255), line_spacing=6):
    lines = []
    current_line = ""

    for char in text:
        test_line = current_line + char
        w = draw.textlength(test_line, font=font)
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char
    if current_line:
        lines.append(current_line)

    # 글자 높이 측정
    line_height = font.getbbox("A")[3] + line_spacing

    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
