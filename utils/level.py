def get_level_info(exp: int):
    level = 1
    base = 100
    required = base

    while exp >= required:
        exp -= required
        level += 1
        required = int(base * (1.5 ** (level - 1)))

    total_required = required
    remaining = total_required - exp

    return {
        "level": level,
        "to_next_level_total_exp": total_required,
        "to_next_level_remaining_exp": remaining
    }
