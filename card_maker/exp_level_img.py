from utils.level import get_level_info


def exp_level_generator(exp,draw, font):
    exp_info = get_level_info(int(exp))

    draw.text((338, 287), str(exp_info["level"]), font=font, fill=(255, 255, 255, 255))

    to_next_level_total = exp_info["to_next_level_total_exp"]
    to_next_level_remain = exp_info["to_next_level_remaining_exp"]

    bar_full_length = 465  # 전체 바 길이
    current_exp = to_next_level_total - to_next_level_remain
    progress_ratio = current_exp / to_next_level_total
    fill_length = int(bar_full_length * progress_ratio)

    box = (25, 370, 25 + fill_length, 423)
    radius = 10
    fill_color = (255, 255, 255, 180)  # 흰색, 알파 180
    draw.rounded_rectangle(box, radius=radius, fill=fill_color)