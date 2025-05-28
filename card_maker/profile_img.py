from utils.pil_util import load_image_from_url, add_rounded_corners


def profile_img_generator(profile_img:str, background):
    profile_img = load_image_from_url(profile_img)
    resized_profile_img = profile_img.resize((169, 169))
    rounded_profile_img = add_rounded_corners(resized_profile_img, radius=20)  # radius는 원하는 만큼 조절
    background.paste(rounded_profile_img, (24, 179), rounded_profile_img)