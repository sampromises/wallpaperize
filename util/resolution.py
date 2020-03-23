import sys
from collections import namedtuple

import bs4
import requests
from cachetools import TTLCache, cached

ONE_DAY_SECONDS = 60 * 60 * 24


class Resolution(namedtuple("Resolution", "width height")):
    pass


@cached(cache=TTLCache(maxsize=8192, ttl=ONE_DAY_SECONDS))
def get_latest_resolutions():
    """
    Fetches list of resolutions from http://screensiz.es/
    """
    response = requests.get("http://screensiz.es/")
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    device_table = soup.find("tbody")
    devices = device_table.find_all("tr")

    results = []
    for device in devices:
        device_name = device.find("td", class_="name").text.strip()
        width = device.find("td", class_="px_width-value").text.strip()
        height = device.find("td", class_="px_height-value").text.strip()
        results.append((f"{width}x{height}", f"{device_name} ({width}x{height})"))
    print(
        f"get_latest_resolutions fetched: {len(results)} items, {sys.getsizeof(results)} total bytes"
    )
    return sorted(results, reverse=True)
