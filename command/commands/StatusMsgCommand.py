from iris import ChatContext

from utils.user_manager import update_about


class StatusMsgCommand:
    invoke = "상메"
    help = "카드 상태메세지를 바꿉니다."
    type = "text"

    def handle(self, event:ChatContext) -> None:
        content = event.message.msg.split(" ", 1)[1]
        update_about(str(event.sender.id), content)
        event.reply(f"{event.sender.name}님의 상태 메세지를 변경했습니다.\n{content}")
