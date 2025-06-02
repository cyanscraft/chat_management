from iris import ChatContext

from api.music_player import player_generator
from api.spotify import get_current_track, spotify_pause, spotify_play, spotify_next, spotify_prev
from command.commands.ICommand import ICommand
from utils.user_manager import update_about


class SpotifyCommand:
    invoke = "spotify"
    help = "개발자용 명령어로 spotify api와 연동하여 현재 재생중인 노래를 컨트롤 하고 노래를 추천합니다."
    type = "text"

    def handle(self, event: ChatContext) -> None:
        args = event.message.msg.strip().split()

        if len(args) < 2:
            result = get_current_track()
            if result == 204:
                event.reply("현재 재생중인 트랙이 없습니다.")
                return
            player = player_generator(result)
            event.reply_media(player)
            return

        command = args[1].lower()

        if command == "play":
            spotify_play()
            event.reply("현재 곡을 재생합니다.")
        elif command == "pause":
            spotify_pause()
            event.reply("현재 재생 중인 곡을 일시정지했습니다.")
        elif command == "next":
            result = spotify_next()
            player = player_generator(result)
            event.reply_media(player)
        elif command == "prev":
            result=spotify_prev()
            player = player_generator(result)
            event.reply_media(player)
        else:
            event.reply(f"알 수 없는 명령어: {command}")
