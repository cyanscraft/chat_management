import re
from typing import Dict

from irispy2 import ChatContext

from command.commands import ICommand
from command.commands.AttendanceCommand import AttendanceCommand
from command.commands.CardCommand import CardCommand
from command.commands.ChangeBackgroundCommand import ChangeBackgroundCommand
from command.commands.StatusMsgCommand import StatusMsgCommand
from command.commands.notification_command import NotificationCommand
from database import notification


class CommandManager:
    def __init__(self):
        self.exact_commands: Dict[str, ICommand] = {}
        print("명령어를 불러오는 중입니다.")
        self.add_command(AttendanceCommand())
        self.add_command(CardCommand())
        self.add_command(StatusMsgCommand())
        self.add_command(NotificationCommand())
        self.add_command(ChangeBackgroundCommand())

    def add_command(self, command: ICommand):
        self.exact_commands[command.invoke] = command
        print(f"☀️ 명령어 등록: {command.invoke}")

    def handle_command(self, event: ChatContext, kl):
        print(f"[메세지] {event.sender.name}: {event.message.msg}")
        prefix = "!"

        if not event.message.msg.startswith(prefix):
            return

        content = event.message.msg[len(prefix):]
        split = content.split()
        if not split:
            return

        invoke = split[0]
        command = self.exact_commands.get(invoke)

        if event.message.msg == "!테스트":
            notification.add_notification(str(event.sender.id), "테스트 알림입니다.")
        if command and command.type == "kl":
            command.handle(event, kl)
        elif command:
            command.handle(event)
