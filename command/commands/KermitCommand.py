import os
import random

from PIL import Image
from iris import ChatContext



base_dir = os.path.dirname(__file__)
folder_path = os.path.join(base_dir, "..","..", "assets", "kermit")
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


class KermitCommand:
    invoke = "커밋"
    help = "랜덤한 커밋 사진을 하나 반환합니다."
    type = "text"

    def handle(self, event:ChatContext):
        selected_file = random.choice(files)
        full_path = os.path.join(folder_path, selected_file)
        event.reply_media(full_path)


