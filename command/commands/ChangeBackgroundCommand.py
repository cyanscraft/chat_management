import json
import time

from iris import ChatContext

from api.s3 import s3_connection, upload_image_from_url


class ChangeBackgroundCommand:
    invoke = "배경"
    help = "유저 카드의 배경을 변경합니다."
    type = "kl"

    def handle(self, event:ChatContext, kl) -> None:
        try:
            raw = event.get_source().raw

            # 문자열이면 json으로 파싱
            if isinstance(raw, str):
                raw = json.loads(raw)

            attachment_str = raw.get("attachment")

            if not attachment_str:
                event.reply("❌ 사진 1장에 답장으로 사용해주세요")
            else:
                type_name=event.get_source().message.msg
                if type_name != "사진": return
                attachment = json.loads(attachment_str)
                attachment_url = attachment.get("url")

                if attachment_url:
                    s3 = s3_connection()
                    print("✅ attachment URL:", attachment_url)
                    upload_img = upload_image_from_url(s3,attachment_url, "studybot", str(int(time.time()))+"jpg", event.sender.id)
                    if upload_img is True:
                        event.reply("이미지가 성공적으로 업로드되었습니다.")
                    else:
                        event.reply("이미지가 너무 큽니다. 3MB이하의 파일만 업로드 가능합니다.")
                else:
                    event.reply("❌ 사진 1장에 답장으로 사용해주세요")

        except json.JSONDecodeError as e:
            event.reply("❌ 사진 1장에 답장으로 사용해주세요:")
        except AttributeError as e:
            event.reply("❌ 사진 1장에 답장으로 사용해주세요:")
        except Exception as e:
            event.reply("❌ 사진 1장에 답장으로 사용해주세요:")

