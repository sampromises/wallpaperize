from collections import namedtuple


class RGB(namedtuple("RGB", "red, green, blue")):
    def hex_format(self):
        red, green, blue = int(self.red), int(self.green), int(self.blue)
        return "#{:02X}{:02X}{:02X}".format(red, green, blue)
