

from typing import List
import requests

from .wikipedia import Section, parseWikipediaPage


def crawlLink(link: str)->  List[Section]:
    if "wikipedia.org" in link:
        response = requests.get(link)
        return parseWikipediaPage(response)

    response = requests.get(link)
    return None