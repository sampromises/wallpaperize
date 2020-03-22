from __future__ import print_function

import binascii
import random
import string

import numpy as np
import scipy
import scipy.cluster
import scipy.misc
from image.color import RGB

NUM_CLUSTERS = 5


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


def get_random_chars():
    length = 16
    allowable_characters = (
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    )
    return "".join(random.choice(allowable_characters) for _ in range(length))


def get_final_filename(filename, res):
    randoms = get_random_chars()
    tokens = filename.split(".")
    name, extension = tokens[0], tokens[-1]
    filename = f"{name}-{res.width}x{res.height}-{randoms}.{extension}"
    filename = filename.replace(" ", "_")
    return filename


def get_image_format(filename):
    try:
        extension = filename.split(".")[-1].upper()
        if extension == "JPG":
            return "JPEG"
        else:
            return extension
    except:
        return "JPEG"
