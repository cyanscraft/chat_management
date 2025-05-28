import time
from urllib.parse import urlencode, quote

import requests
from iris import ChatContext

from utils.user_manager import get_or_create


class CardCommand:
    invoke = "카드"
    help = "유저 카드를 가져옵니다"
    type = "kl"

    def handle(self, event:ChatContext, kl) -> None:
        data = {
            "userid": event.sender.id,
            "name": quote(event.sender.name),
            "bot_url": event.url,
            "timestamp": int(time.time())
        }
        query = urlencode(data)
        kl.send(
                receiver_name=event.room.name,
                template_id=4718,
                template_args={
                    "imageUrl": f"{event.img_url}/user?{query}"
                },
            )

