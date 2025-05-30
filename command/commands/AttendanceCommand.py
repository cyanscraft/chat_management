from iris import ChatContext
from utils.user_manager import handle_attendance

def format_attendance_message(data):
    return f"""\n  🏅 오늘의 출석 랭킹: {data['attend_rank']}위\n  🔥 연속 출석: {data['stream_count']}일\n  📈 누적 출석: {data['total_attend_count']}회\n  🪙exp: {data["exp"]}\n"""


class AttendanceCommand:
    invoke = "출석"
    help = "유저 카드를 가져옵니다"
    type = "kl"

    def handle(self, event:ChatContext, kl) -> None:
        result=handle_attendance(str(event.sender.id),event.sender.name)
        if not result["success"]:
            event.reply("\n⚠️ 이미 오늘 출석했습니다. ⚠️\n"+format_attendance_message(result))
        else:
            event.reply( "\n  🎉 출석 완료! 🎉"+format_attendance_message(result))

# 출석 시간체크 -> 뱃지지급
# 출석 랭킹 체크 -> 뱃지지급
