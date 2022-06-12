from ctypes import Union
from typing import List
from bs4 import BeautifulSoup
from pyparsing import Optional
import requests


class Section(object):
    heading: str
    paragraphs: list
    link: str
    keywords: List[tuple[str, float, tuple[float, str]]]

    def __init__(self, heading: str, link:str, paragraphs = []) -> None:
        self.heading = heading
        self.paragraphs = paragraphs
        self.link = link
        self.keywords = []
    
    def __repr__(self):
        return f"Section(heading={self.heading}, numOfParagraphs={len(self.paragraphs)})"

    def __str__(self):
        return f"Section(heading={self.heading}, numOfParagraphs={len(self.paragraphs)})"
        
    def toJson(self):
        return {"heading": self.heading, "paragraphs": self.paragraphs, "link": self.link, "keywords": list(map(lambda x: {"kw": x[0], "score": x[1], "distance": {"score": x[2][0], "alg": x[2][1]}}, self.keywords))}

    def get_text(self):
        return ' '.join(self.paragraphs)
    def set_keywords(self, keywords_scored_distanced):
        self.keywords = keywords_scored_distanced

def find_all_description_metas(tag):
    return tag.name =="meta" and (tag.get("name") == "description" or tag.get("property") == "og:description")

def parseGeneral(soup: BeautifulSoup, entity_mame: str) -> tuple[str, List[str]]:
    # soup = BeautifulSoup(page.content, 'html.parser')
    metaTags = soup.find_all(find_all_description_metas)
    paragraphs = list(set([tag.get("content") for tag in metaTags]))

    heading = entity_mame
    if soup.title:
        heading = soup.title.get_text()

    return heading, paragraphs
