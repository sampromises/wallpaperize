import os
import random
import string

from image.util import get_most_frequent_color
from PIL import Image


def get_background(color, res):
    image = Image.new("RGB", (res.width, res.height), color)
    return image


def get_resized_resolution(image_resolution, bg_resolution):
    """Return a resized image that fits completely within a given resolution"""
    img_x, img_y = image_resolution
    bg_x, bg_y = bg_resolution

    if img_x > bg_x or img_y > bg_y:  # Image shrinks
        if img_x > bg_x and img_y > bg_y:  # Image larger in both dimensions
            if abs(img_x - bg_x) > abs(img_y - bg_y):
                scale = bg_x / img_x
            else:
                scale = bg_y / img_y
        elif img_x > bg_x:  # Image larger in width
            scale = bg_x / img_x
        elif img_y > bg_y:  # Image larger in height
            scale = bg_y / img_y
        else:
            raise Exception("Uncaught case")
        return round(img_x * scale), round(img_y * scale)
    else:  # Image enlarges
        if abs(img_x - bg_x) < abs(img_y - bg_y):  # Scale in X direction
            scale = bg_x / img_x
        else:  # Scale in Y direction
            scale = bg_y / img_y
        return round(img_x * scale), round(img_y * scale)


def resize_image(image, bg_resolution):
    """Return a resized image that fits completely within a given resolution"""
    old_width, old_height = image.size
    new_width, new_height = get_resized_resolution(
        image.size, (bg_resolution.width, bg_resolution.height)
    )
    if new_width < old_width or new_height < old_height:  # Image shrinks
        print("Image shrinks")
        resized = image.copy()
        resized.thumbnail((new_width, new_height), Image.ANTIALIAS)
        return resized
    else:  # Image enlarges
        print("Image enlarges")
        resized = image.resize((new_width, new_height), Image.ANTIALIAS)
        return resized


def get_center(resolution):
    return resolution.width // 2, resolution.height // 2


def _get_random_chars():
    length = 8
    allowable_characters = (
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    )
    return "".join(random.choice(allowable_characters) for _ in range(length))


def get_wallpaper_filename(filename, res):
    basename, extension = os.path.splitext(filename)
    filename = f"{basename}-{res.width}x{res.height}-{_get_random_chars()}" + extension
    return filename


def create_wallpaper(image, resolution, background_color=None):
    resized_image = resize_image(image, resolution)

    if background_color is None:
        background_color = get_most_frequent_color(image)

    cx, cy = get_center(resolution)
    width, height = resized_image.size
    wallpaper = get_background(background_color, resolution)
    wallpaper.paste(resized_image, (cx - width // 2, cy - height // 2))

    return wallpaper
