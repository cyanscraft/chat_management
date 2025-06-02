import os
from collections import defaultdict

from google import genai
gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)
from iris import ChatContext

history_cache = defaultdict(list)

class GeminiCommand:
    invoke = "먀"
    help = "!ai명령어로 ai와 대화할 수 있습니다."
    type = "text"

    def handle(self, event: ChatContext):
        user_id = event.sender.id
        content = event.message.msg[len("!먀 "):].strip()

        # (선택) “초기화” 명령어 처리
        if content == "초기화":
            history_cache[user_id] = []
            event.reply("💬 대화 기록이 초기화되었습니다.")
            return

        # 3) 기존 히스토리 불러오기 (리스트 형태)
        history = history_cache[user_id]

        # 4) 유저 메시지를 “딕셔너리” 포맷으로 history에 추가
        history.append({
            "role": "user",
            "parts": [{"text": content}]
        })

        # 5) 최신 기록(딕셔너리 리스트)을 그대로 넘겨서 generate_content 호출
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=history
        )

        # 6) 모델 응답을 같은 포맷으로 히스토리에 추가
        history.append({
            "role": "model",
            "parts": [{"text": response.text}]
        })

        # 7) 너무 길어지지 않도록, 최근 10개 메시지만 유지
        history_cache[user_id] = history[-10:]

        # 8) 사용자에게 응답 전송
        event.reply(response.text)