import os
import re

from dotenv import load_dotenv
from iris import ChatContext
from database.chat_logs import get_chat_logs
from google import genai
invisible = "\u200b" * 500

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)

class SummaryCommand:
    invoke = "요약"
    help = "!방별로 안읽은 채팅들을 요약해줍니다."
    type = "text"

    def handle(self, event: ChatContext, session):
        msg = event.message.msg.strip()
        match = re.fullmatch(r"!요약\s+(\d+)", msg)

        if match:
            selected_number = int(match.group(1))
            session_items = list(session.items())

            if 1 <= selected_number <= len(session_items):
                room_id, room_data = session_items[selected_number - 1]
                if "start_id" not in room_data:
                    event.reply("시작 키가 없어 초기화를 시작했습니다.")
                    room_data["start_id"] = event.message.id
                else:
                    chat_logs = get_chat_logs(
                        url=event.url,
                        start_id=room_data["start_id"],
                        end_id=room_data["end_id"],
                        room_id=room_id
                    )

                    chat_count = len(chat_logs)
                    event.reply(f"{chat_count - 2}개의 대화를 요약하는 중입니다....")

                    summary_input = "\n".join(
                        f"{log['nickname']}: {log['message']}"
                        for log in chat_logs if log.get("message")
                    )

                    room_data["start_id"] = event.message.id

                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents="다음 채팅을 요약해줘. 위쪽에는 대화의 전체 내용을 요약해주고. 아래에는 대화 참여자와 참여자들의 특징을 요약해줘, 비중같은것도 나타내주고 또한 제일 위와 아래 채팅인 '!요약'은 빼고 해줘\n" + summary_input,
                    )

                    event.reply(f"{chat_count - 2}건의 채팅을 요약했습니다." + invisible + "\n\n" + response.text)
            else:
                event.reply("❌ 잘못된 번호입니다.")
        else:
            room_names = [
                f"{idx + 1}. {room_data['name']}"
                for idx, room_data in enumerate(session.values())
            ]
            event.reply(
                "어느 방의 채팅을 요약하시겠어요?\n\n" +
                "\n".join(room_names) +
                "\n\n📌 '!요약 <숫자>' 형식으로 입력해주세요."
            )


def handle(self, event: ChatContext, session):
    msg = event.message.msg.strip()
    match = re.fullmatch(r"!요약\s+(\d+)", msg)

    if match:
        selected_number = int(match.group(1))
        session_items = list(session.items())

        if 1 <= selected_number <= len(session_items):
            room_id, room_data = session_items[selected_number - 1]
            event.reply(f"✅ '{room_data['name']}' 방의 요약을 시작합니다.")

            if "start_id" not in room_data:
                event.reply("시작 키가 없어 초기화를 시작했습니다.")
                room_data["start_id"] = event.message.id
            else:
                chat_logs = get_chat_logs(
                    url=event.url,
                    start_id=room_data["start_id"],
                    end_id=room_data["end_id"],
                    room_id=room_id
                )

                chat_count = len(chat_logs)
                event.reply(f"{chat_count - 2}개의 대화를 요약하는 중입니다....")

                summary_input = "\n".join(
                    f"{log['nickname']}: {log['message']}"
                    for log in chat_logs if log.get("message")
                )

                room_data["start_id"] = event.message.id

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents="다음 채팅을 요약해줘. 위쪽에는 대화의 전체 내용을 요약해주고. 아래에는 대화 참여자와 참여자들의 특징을 요약해줘, 비중같은것도 나타내주고 또한 제일 위와 아래 채팅인 '!요약'은 빼고 해줘\n" + summary_input,
                )

                event.reply(f"{chat_count - 2}건의 채팅을 요약했습니다." + invisible + "\n\n" + response.text)
        else:
            event.reply("❌ 잘못된 번호입니다.")
    else:
        room_names = [
            f"{idx + 1}. {room_data['name']}"
            for idx, room_data in enumerate(session.values())
        ]
        event.reply(
            "어느 방의 채팅을 요약하시겠어요?\n\n" +
            "\n".join(room_names) +
            "\n\n📌 '!요약 <숫자>' 형식으로 입력해주세요."
        )
