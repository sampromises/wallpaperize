from collections import namedtuple

from image.resolution import Resolution
from image.util import get_final_filename


def test_get_final_filename():
    res = Resolution(1, 2)
    assert f"foo-1x2.txt" == get_final_filename("foo.txt", res)
    assert f"foo%20bar-1x2.txt" == get_final_filename("foo bar.txt", res)
    assert f"foo%2Cbar-1x2.txt" == get_final_filename("foo,bar.txt", res)
    assert f"foo.bar-1x2.txt" == get_final_filename("foo.bar.txt", res)
