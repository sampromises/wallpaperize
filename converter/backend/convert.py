from collections import namedtuple
from converter.backend.util import get_most_frequent_color
from PIL import Image


def get_background(color, res):
    image = Image.new('RGB', (res.width, res.height), color)
    return image


def resize_image(image, bg_resolution):
    """Return a resized image that fits completely within a given resolution"""
    img_x, img_y = image.size
    bg_x, bg_y = bg_resolution.width, bg_resolution.height

    if img_x > bg_x or img_y > bg_y:  # Image shrinks
        if img_x > bg_x and img_y > bg_y:  # Image larger in both dimensions
            if abs(img_x - bg_x) > abs(img_y - bg_y):
                length = bg_x
            else:
                length = bg_y
        elif img_x > bg_x:  # Image larger in width
            length = bg_x
        else:  # Image larger in height
            length = bg_y
        resized = image.copy()
        resized.thumbnail((length, length), Image.ANTIALIAS)
        return resized
    else:  # Image enlarges
        if abs(img_x - bg_x) < abs(img_y - bg_y):  # Scale in X direction
            scale = bg_x / img_x
        else:  # Scale in Y direction
            scale = bg_y / img_y
        x, y = round(img_x * scale), round(img_y * scale)
        resized = image.resize((x, y), Image.ANTIALIAS)
        return resized


def get_center(resolution):
    return resolution.width // 2, resolution.height // 2


def create_wallpaper(image, resolution, background_color=None):
    # image = Image.open(image_path)
    resized_image = resize_image(image, resolution)

    if background_color is None:
        background_color = get_most_frequent_color(image)

    cx, cy = get_center(resolution)
    width, height = resized_image.size
    background = get_background(background_color, resolution)
    background.paste(resized_image, (cx - width // 2, cy - height // 2))

    return background
