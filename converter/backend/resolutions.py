from collections import namedtuple

resolution = namedtuple("resolution", ["name", "width", "height"])

IPHONE_XS = resolution(name="iphone-xs", width=1125, height=2436)
IPHONE_7P = resolution(name="iphone-7p", width=1080, height=1920)
MBPRO_2015_13 = resolution(name="macbookpro-13-2015", width=2560, height=1600)
HD_1080 = resolution(name="1080p", width=1920, height=1080)
THUMBNAIL = resolution(name="thumbnail-500", width=500, height=500)
