from collections import namedtuple
from enum import Enum

resolution = namedtuple("resolution", ["name", "width", "height"])


class Resolution(Enum):
    IPHONE_X_XS = resolution(name="iPhone X/XS (1125x2436)", width=1125, height=2436)
    IPHONE_XS_MAX = resolution(name="iPhone XS Max (1242x2688)", width=1242, height=2688)
    IPHONE_7_8 = resolution(name="iPhone 7/8 (750x1334)", width=750, height=1334)
    IPHONE_7_8_PLUS = resolution(name="iPhone 7/8 Plus (1080x1920)", width=1080, height=1920)
    IPAD_PRO = resolution(name="iPad Pro (2048x2732)", width=2048, height=2732)
    IPAD_3_4 = resolution(name="iPad Third & Fourth Generation (1536x2048)", width=1536, height=2048)
    MBPRO_13 = resolution(name="Macbook Pro 13-inch (2560x1600)", width=2560, height=1600)
    MBPRO_15 = resolution(name="Macbook Pro 15-inch (2880x1800)", width=1880, height=1800)
    MBPRO_16 = resolution(name="Macbook Pro 16-inch (3072x1920)", width=3072, height=1920)
    THUMBNAIL = resolution(name="Thumbnail (500x500)", width=500, height=500)
    HD = resolution(name="HD (720x480)", width=720, height=480)
    FHD = resolution(name="FHD (1920x1080)", width=1920, height=1080)
    QHD = resolution(name="QHD (2560x1440)", width=2560, height=1440)
    FOUR_K = resolution(name="4K (3840x2160)", width=3840, height=2160)
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
