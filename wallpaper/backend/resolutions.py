from collections import namedtuple
from enum import Enum

resolution = namedtuple("resolution", ["name", "width", "height"])


class Resolution(Enum):
    IPHONE_X_XS = resolution(name='iPhone X/XS', width=1125, height=2436)
    IPHONE_XS_MAX = resolution(name='iPhone XS Max', width=1242, height=2688)
    IPHONE_7_8 = resolution(name='iPhone 7/8', width=750, height=1334)
    IPHONE_7_8_PLUS = resolution(name='iPhone 7/8 Plus', width=1080, height=1920)
    IPAD_PRO = resolution(name='iPad Pro', width=2048, height=2732)
    IPAD_3_4 = resolution(name='iPad Third & Fourth Generation', width=1536, height=2048)
    MBPRO_2015_13 = resolution(name='Macbook Pro 2015 13"', width=2560, height=1600)
    THUMBNAIL = resolution(name='Thumbnail', width=500, height=500)
    HD_1080 = resolution(name='1080p', width=1920, height=1080)
    HD_720 = resolution(name='720p', width=720, height=480)
    DEFAULT = IPHONE_7_8_PLUS

    @property
    def name(self):
        return self.value.name

    @property
    def width(self):
        return self.value.width

    @property
    def height(self):
        return self.value.height


@property
def default(self):
    return self.HD_720
