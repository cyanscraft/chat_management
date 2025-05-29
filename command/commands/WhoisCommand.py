from iris import ChatContext

from utils.user_manager import update_about


class WhoisCommand:
    invoke = "누구"
    help = "해당 사진이 누구인지 분석합니다.."
    type = "text"

    def handle(self, event:ChatContext) -> None:
        ...