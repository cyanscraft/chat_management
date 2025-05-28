import json
import os
from datetime import datetime, time

base_dir = os.path.dirname(__file__)
badge_path = os.path.join(base_dir, "..", "assets", "badge.json")

with open(badge_path, "r", encoding="utf-8") as f:
    badges = json.load(f)["badges"]

def check_role(user, value):
    return value in user.get("roles", [])


def check_date(user, value):
    today = datetime.now()
    month, day = map(int, value.split("-"))
    return today.month == month and today.day == day


def check_time(user, value):
    now = datetime.now().time()
    start_str, end_str = value.split("-")
    start = datetime.strptime(start_str, "%H:%M").time()
    end = datetime.strptime(end_str, "%H:%M").time()
    return start <= now <= end


def check_rank(user, value):
    return user.get("rank", 0) == int(value)


def check_first_post_dev(user, value):
    return user.get("is_first_post_dev", False) == bool(value)


def check_streak_days(user, value):
    return user.get("streak_days", 0) >= int(value)


def check_checkin_attempts(user, value):
    return user.get("checkin_attempts", 0) >= int(value)


def check_chat_count(user, value):
    return user.get("chat_count", 0) >= int(value)


# 조건 타입별 함수 매핑
check_funcs = {
    "role": check_role,
    "date": check_date,
    "time": check_time,
    "rank": check_rank,
    "first_post_dev": check_first_post_dev,
    "streak_days": check_streak_days,
    "checkin_attempts": check_checkin_attempts,
    "chat_count": check_chat_count,
}


def check_badge_condition(user, badge):
    cond_type = badge['condition']['type']
    cond_value = badge['condition']['value']

    checker = check_funcs.get(cond_type)
    if not checker:
        return False

    return checker(user, cond_value)


def get_earned_badges(user):
    earned = []
    for badge in badges:
        if check_badge_condition(user, badge):
            earned.append(badge)
    return earned


# ==== 테스트 ====

user_data = {
    "roles": ["member", "owner"],
    "rank": 1,
    "is_first_post_dev": True,
    "streak_days": 10,
    "chat_count": 150,
}

earned_badges = get_earned_badges(user_data)

