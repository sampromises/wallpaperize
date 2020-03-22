from image.util import parse_resolution


def test_parse_resolution():
    assert (2560, 1600) == parse_resolution("Macbook Pro 13-inch (2560x1600)")
    assert (1920, 1080) == parse_resolution("1920x1080")
    assert (1920, 1080) == parse_resolution("1920 x 1080")
    assert (1280, 720) == parse_resolution("1280,720")
    assert (1280, 720) == parse_resolution("1280 720")
    assert (3840, 2160) == parse_resolution("4K (3840x2160)")
