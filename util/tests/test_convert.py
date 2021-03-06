from util.convert import _get_resized_resolution

BG_RESOLUTION = (100, 100)  # Fixed

# WIDTH, HEIGHT
# SHORTER, SAME, LONGER

"""
Image width > background width
"""


def test_longer_width_shorter_height():
    img_resolution = (150, 50)
    assert (100, 33) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


def test_longer_width_same_height():
    img_resolution = (150, 100)
    assert (100, 67) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


def test_longer_width_longer_height():
    img_resolution = (150, 150)
    assert (100, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)

    img_resolution = (200, 150)
    assert (100, 75) == _get_resized_resolution(img_resolution, BG_RESOLUTION)

    img_resolution = (150, 200)
    assert (75, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


"""
Image width == background width
"""


def test_same_width_shorter_height():
    img_resolution = (100, 50)
    assert (100, 50) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


def test_same_width_same_height():
    img_resolution = (100, 100)
    assert (100, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


def test_same_width_longer_height():
    img_resolution = (100, 150)
    assert (67, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


"""
Image width < background width
"""


def test_shorter_width_shorter_height():
    img_resolution = (50, 25)
    assert (100, 50) == _get_resized_resolution(img_resolution, BG_RESOLUTION)

    img_resolution = (50, 50)
    assert (100, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)

    img_resolution = (50, 75)
    assert (67, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)

    assert (920, 1080) == _get_resized_resolution((409, 480), (1920, 1080))


def test_shorter_width_same_height():
    img_resolution = (50, 100)
    assert (50, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)


def test_shorter_width_longer_height():
    img_resolution = (50, 150)
    assert (33, 100) == _get_resized_resolution(img_resolution, BG_RESOLUTION)
