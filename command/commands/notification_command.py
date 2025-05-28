from datetime import datetime

from iris import ChatContext

from database.notification import get_unread_notifications, get_recent_notifications, mark_notifications_read

invisible = "\u200b" * 500

def format_notifications(user_id: str, user_name: str):
    notifications = get_recent_notifications(user_id)
    invisible = "\u200b" * 500  # 더보기를 유도하는 invisible 문자

    header = f"🔔 {user_name}님의 알림함 {invisible}\n\n(최근 50개만 표시됩니다.)\n\n"

    if not notifications:
        return header + "📭 현재 받은 알림이 없습니다."

    lines = []
    for notif_id, message, read, ts in notifications:
        status = "✅" if read else "🆕"
        time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        lines.append(f"{status} [{time_str}] {message}")

    return header + "\n".join(lines)

class NotificationCommand:
    invoke = "알림"
    help = "수신된 알림을 보여줍니다."
    type="text"

    def handle(self, event:ChatContext) -> None:
        result = format_notifications(str(event.sender.id), event.sender.name)
        event.reply(result)
        mark_notifications_read(str(event.sender.id))
        '''
        unreads = get_unread_notifications(str(event.sender.id))
        if len(unreads) > 0:
            event.reply(f"🔔 {event.sender.name}님 안 읽은 알림이 {len(unreads)}개 있습니다!{invisible}")
            '''


