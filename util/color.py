from __future__ import print_function

import binascii
from collections import namedtuple

import numpy as np
import scipy
import scipy.cluster
import scipy.misc

NUM_CLUSTERS = 5


class RGB(namedtuple("RGB", "red, green, blue")):
    def hex_format(self):
        red, green, blue = int(self.red), int(self.green), int(self.blue)
        return "#{:02X}{:02X}{:02X}".format(red, green, blue)

    @staticmethod
    def from_hex(_hex):
        return RGB(*tuple(int(_hex[i : i + 2], 16) for i in (0, 2, 4)))


def get_most_frequent_color(im):
    """Gets most common color, as hex"""
    # im = Image.open(image_path)
    im = im.convert("RGB")
    im = im.resize((150, 150))  # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape

    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))  # count occurrences

    index_max = scipy.argmax(counts)  # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode("ascii")

    return RGB(int(peak[0]), int(peak[1]), int(peak[2]))
