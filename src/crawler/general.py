from ctypes import Union
from typing import List
from bs4 import BeautifulSoup
from pyparsing import Optional
import requests


class Section(object):
    heading: str
    paragraphs: list
    link: str

    def __init__(self, heading: str, link:str, paragraphs = []) -> None:
        self.heading = heading
        self.paragraphs = paragraphs
        self.link = link
    
    def __repr__(self):
        return f"Section(heading={self.heading}, numOfParagraphs={len(self.paragraphs)})"

    def __str__(self):
        return f"Section(heading={self.heading}, numOfParagraphs={len(self.paragraphs)})"
        
    def toJson(self):
        return {"heading": self.heading, "paragraphs": self.paragraphs, "link": self.link}

def parseGeneral(soup: BeautifulSoup, entity_mame: str) -> tuple[str, List[str]]:
    # soup = BeautifulSoup(page.content, 'html.parser')
    metaTags = soup.find_all("meta", {"name": "description"})
    paragraphs = [tag.get("content") for tag in metaTags]

    heading = entity_mame
    if soup.title:
        heading = soup.title.get_text()

    return heading, paragraphs
