import os
import threading
from iris import Bot, ChatContext, IrisLink
from iris.bot.models import ErrorContext

from command.CommandManager import CommandManager
from utils.user_manager import update_chat_count


bot_url = "http://146.56.160.198:3000"
bot = Bot(iris_url=bot_url)
manager = CommandManager()

@bot.on_event("message")
def on_message(chat: ChatContext):
    chat.url = bot_url
    manager.handle_command(chat,kl)
    update_chat_count(chat)

@bot.on_event("error")
def on_error(err: ErrorContext):
    print(err.event, "이벤트에서 오류가 발생했습니다", err.exception)


if __name__ == "__main__":
    kl = IrisLink(bot.iris_url)
    bot.run()

