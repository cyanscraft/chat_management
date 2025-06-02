import io
import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

from api.spotify import get_current_track

base_dir = os.path.dirname(__file__)
template_path = os.path.join(base_dir, "..", "assets", "spotify","template.png")

def truncate_text(text, font, max_width):
    ellipsis = "..."
    ellipsis_width = font.getlength(ellipsis)

    # 원래 텍스트가 제한보다 짧으면 그대로 반환
    if font.getlength(text) <= max_width:
        return text

    # 길이가 넘으면 잘라가면서 ... 붙이기
    while font.getlength(text) + ellipsis_width > max_width:
        if len(text) <= 1:
            return ellipsis
        text = text[:-1]

    return text + ellipsis

def wrap_text(text, font, max_width, draw):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def load_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # 실패시 예외 발생
    return Image.open(BytesIO(response.content)).convert("RGBA")

def font_path(fontname):
    font_url = os.path.join(base_dir, "..", "assets", "fonts", fontname + ".ttf")
    return os.path.abspath(font_url)

def ms_to_mmss(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02}:{remaining_seconds:02}"

def player_generator(track_info):
    progress_ms = track_info["progress_ms"]  # 현재 듣고있는 시간
    track_name = track_info["item"]["name"]
    artists = ", ".join([a["name"] for a in track_info["item"]["artists"]])
    album_name = track_info["item"]["album"]["name"]
    duration_ms = track_info["item"]["duration_ms"]
    album_art = track_info["item"]["album"]["images"][0]["url"]

    template = Image.open(template_path).convert("RGBA")

    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(font_path("NotoSansKR-Bold"), 23)  # 크기 36

    y = 148
    lines = wrap_text(track_name, font, 280, draw)
    for line in lines:
        draw.text((340, y), line, font=font, fill=(255, 255, 255, 255))
        y += font.size + 2

    font = ImageFont.truetype(font_path("NotoSansKR-Medium"), 23)
    artist_text = truncate_text(artists, font, 260)
    draw.text((340, 223), artist_text, font=font, fill=(255, 255, 255, 255))

    y = 267
    lines = wrap_text(album_name, font, 280, draw)
    for line in lines:
        draw.text((340, y), line, font=font, fill=(255, 255, 255, 255))
        y += font.size + 2

    ratio=progress_ms/duration_ms
    box = (46, 393, 46+510*ratio, 399)
    fill_color = (70, 181, 105, 255)  # 흰색, 알파 180
    draw.rounded_rectangle(box, radius=3, fill=fill_color)

    album_img = load_image_from_url(album_art).resize((240, 240))
    template.paste(album_img, (45, 135), album_img)

    font = ImageFont.truetype(font_path("NotoSansKR-Medium"), 24)
    draw.text((45, 403), ms_to_mmss(progress_ms), font=font, fill=(160, 160, 160, 255))
    draw.text((498, 403), ms_to_mmss(duration_ms), font=font, fill=(160, 160, 160, 255))

    buf = io.BytesIO()
    template.save(buf, format="PNG")
    buf.seek(0)
    return buf

if __name__ == '__main__':
    current = get_current_track()
    player_generator(current)
