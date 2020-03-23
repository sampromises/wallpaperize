from collections import namedtuple


class RGB(namedtuple("RGB", "red, green, blue")):
    def hex_format(self):
        red, green, blue = int(self.red), int(self.green), int(self.blue)
        return "#{:02X}{:02X}{:02X}".format(red, green, blue)

    @staticmethod
    def from_hex(_hex):
        return RGB(*tuple(int(_hex[i : i + 2], 16) for i in (0, 2, 4)))
