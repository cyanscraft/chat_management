import re
from typing import Dict

from irispy2 import ChatContext

from command.commands import ICommand
from command.commands.AttendanceCommand import AttendanceCommand
from command.commands.CardCommand import CardCommand
from command.commands.ChangeBackgroundCommand import ChangeBackgroundCommand
from command.commands.GeminiCommand import GeminiCommand
from command.commands.KermitCommand import KermitCommand
from command.commands.SpotifyCommand import SpotifyCommand
from command.commands.StatusMsgCommand import StatusMsgCommand
from command.commands.SummaryCommand import SummaryCommand
from command.commands.WeatherCommand import WeatherCommand
from command.commands.WhoisCommand import WhoisCommand
from command.commands.notification_command import NotificationCommand

session = {}

class CommandManager:
    def __init__(self):
        self.exact_commands: Dict[str, ICommand] = {}
        print("명령어를 불러오는 중입니다.")
        self.add_command(AttendanceCommand())
        self.add_command(CardCommand())
        self.add_command(StatusMsgCommand())
        self.add_command(NotificationCommand())
        self.add_command(ChangeBackgroundCommand())
        self.add_command(WhoisCommand())
        self.add_command(WeatherCommand())
        self.add_command(KermitCommand())
        self.add_command(SummaryCommand())
        self.add_command(SpotifyCommand())
        self.add_command(GeminiCommand())

    def add_command(self, command: ICommand):
        self.exact_commands[command.invoke] = command
        print(f"☀️ 명령어 등록: {command.invoke}")

    def handle_command(self, event: ChatContext, kl):
        session.setdefault(str(event.room.id), {})
        session[str(event.room.id)]["name"] = event.room.name
        session[str(event.room.id)]["end_id"] = event.message.id
        if "start_id" not in session[str(event.room.id)]:
            session[str(event.room.id)]["start_id"] = event.message.id

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

        if invoke == "su":
            command.handle(event, session)
            return
        if command and command.type == "kl":
            command.handle(event, kl)
        elif command:
            command.handle(event)
