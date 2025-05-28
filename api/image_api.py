import json
import os
from urllib.parse import unquote

import requests
from PIL import Image, ImageDraw, ImageFont
import io

from card_maker.exp_level_img import exp_level_generator
from card_maker.profile_img import profile_img_generator
from users.user import get_open_chat_member
from utils.badge import get_badges
from utils.level import get_level_info
from utils.pil_util import draw_wrapped_text, load_image_from_url, add_rounded_corners, resize_cover
from utils.user_manager import get_or_create

# emplate = template.resize((800, 800))
base_dir = os.path.dirname(__file__)
base_path = os.path.join(base_dir, "..", "assets", "img.png")
template_path = os.path.join(base_dir, "..", "assets", "template.png")

def font_path(fontname):
    font_url = os.path.join(base_dir, "..", "assets", "fonts", fontname + ".ttf")
    return os.path.abspath(font_url)

badge_path = os.path.join(base_dir, "..", "assets", "badge.json")
badge_sheet_path = os.path.join(base_dir, "..", "assets", "badge_sheet.png")

with open(badge_path, "r", encoding="utf-8") as f:
    badge_data = json.load(f)["badges"]

sprite_sheet = Image.open(badge_sheet_path).convert("RGBA")
badge_dict = {b["id"]: b for b in badge_data}

def generate_image(userid, name, bot_url) -> bytes:
    chat_member = get_open_chat_member(userid, bot_url)
    profile_img = chat_member["profile_image_url"]
    user_type = chat_member["link_member_type"]
    user_data = get_or_create(userid, name)
    exp = str(user_data["exp"])
    exp_rank = str(user_data["exp_rank"])
    chat_count = str(user_data["chat_count"])
    attend_rank = str(user_data["attend_rank"])
    about = user_data["about"]
    background_url = f"https://studybot.s3.ap-northeast-2.amazonaws.com/{user_data["background_url"]}"


    background = Image.new("RGBA", (800, 800), color=(255, 255, 255, 255))

    if user_data["background_url"]:
        bg_by_link=load_image_from_url(background_url)
        resized_base=resize_cover(bg_by_link,(800,800))
        background.alpha_composite(resized_base)
    else:
        base_img = Image.open(base_path).convert("RGBA")
        resized_base = resize_cover(base_img, size=(800, 800))
        background.alpha_composite(resized_base)

    template = Image.open(template_path).convert("RGBA")
    background.alpha_composite(template)

    profile_img_generator(profile_img, background)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(font_path("NotoSansKR-Bold"), 65)  # 크기 36
    draw.text((215, 190), unquote(name), font=font, fill=(255, 255, 255, 255))

    font_small = ImageFont.truetype(font_path("NotoSansKR-Bold"), 36)  # RANK용
    font_large = ImageFont.truetype(font_path("NotoSansKR-Black"), 65)  # #90용
    rank_text = "#" +  str(exp_rank)
    prefix_text = "RANK "
    prefix_width = draw.textlength(prefix_text, font=font_small)
    y_base = 10
    draw.text((10, y_base + 34), prefix_text, font=font_small, fill=(255, 255, 255, 255))  # 작은 텍스트는 약간 내려
    draw.text((10 + prefix_width, y_base), rank_text, font=font_large, fill=(255, 255, 255, 255))

    font_attend = ImageFont.truetype(font_path("NotoSansKR-Black"), 32)
    draw.text((573, 370), "출석 " + str(attend_rank) + "등", font=font_attend, fill=(255, 255, 255, 255))

    font_attend = ImageFont.truetype(font_path("NotoSansKR-Black"), 30)

    exp_width = draw.textlength(exp, font=font_attend)
    chat_width = draw.textlength(chat_count, font=font_attend)

    right_margin_x = 490

    exp_x = right_margin_x - exp_width
    chat_x = right_margin_x - chat_width

    # 텍스트 그리기
    draw.text((exp_x, 445), exp, font=font_attend, fill=(255, 255, 255, 255))
    draw.text((chat_x, 498), chat_count, font=font_attend, fill=(255, 255, 255, 255))

    text = about
    font_attend = ImageFont.truetype(font_path("NotoSansKR-Bold"), 28)

    draw_wrapped_text(draw, text, font_attend, 80, 600, 410, fill=(255, 255, 255, 255), line_spacing=6)

    font = ImageFont.truetype(font_path("NotoSansKR-Medium"), 39)
    exp_level_generator(exp, draw, font)

    #==========
    badges = get_badges(userid)
    if user_type == "1":
        badges.insert(0,1)
    elif user_type == "4":
        badges.insert(0,2)
    for idx, badge_id in enumerate(badges):
        badge = badge_dict.get(badge_id)
        if not badge:
            continue  # 없는 ID는 건너뜀

        x, y, w, h = badge["icon"]
        cropped_icon = sprite_sheet.crop((x, y, x + w, y + h))

        cols = 3
        row = idx // cols
        col = idx % cols

        paste_x = 540 + col * (80)
        paste_y = row * (90)
        background.paste(cropped_icon, (paste_x, 450+paste_y), cropped_icon)  # 알파 채널 유지

    #==========
    buffer = io.BytesIO()
    background.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

