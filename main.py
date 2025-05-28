import os
import threading
from iris import Bot, ChatContext, IrisLink
from iris.bot.models import ErrorContext

from command.CommandManager import CommandManager
from api.server import app as api_app
from utils.user_manager import update_chat_count


bot_url = "http://146.56.160.198:3000"
img_url = "http://localhost:5000"
bot = Bot(iris_url=bot_url)
manager = CommandManager()

@bot.on_event("message")
def on_message(chat: ChatContext):
    chat.url = bot_url
    chat.img_url = img_url
    manager.handle_command(chat,kl)
    update_chat_count(chat)

@bot.on_event("error")
def on_error(err: ErrorContext):
    print(err.event, "이벤트에서 오류가 발생했습니다", err.exception)

def run_api():
    api_app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    kl = IrisLink(bot.iris_url)
    threading.Thread(target=run_api, daemon=True).start()
    bot.run()

