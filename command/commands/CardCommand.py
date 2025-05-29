from iris import ChatContext

from api.image_api import generate_image

class CardCommand:
    invoke = "카드"
    help = "유저 카드를 가져옵니다"
    type = "kl"

    def handle(self, event:ChatContext, kl) -> None:
        img=generate_image(event.sender.id, event.sender.name, event.url)
        event.reply("⚠️ "+event.sender.name+"님의 카드 생성중....")
        event.reply_media(img)

        '''
        data = {
            "userid": event.sender.id,
            "username": quote(event.sender.name),
            "timestamp": int(time.time()),
            "user_type":user["link_member_type"]
        }
        query = urlencode(data)


        kl.send(
                receiver_name=event.room.name,
                template_id=115564,
                template_args={
                    "THU": f"https://ondojung.mycafe24.com/api/user/card.php?{query}"
                },
            )
'''
