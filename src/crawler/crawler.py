

from typing import List
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from crawler.general import Section, parseGeneral

from .wikipedia import parseWikipediaPage

def is_in_english(soup: BeautifulSoup) -> bool:
    return soup.html["lang"] == "en"
    
def crawlLink(link: str, entity_name: str) -> tuple[str, List[str]]:
    print("crawling", link)
    session = HTMLSession()
    response = session.get(link)

    print("parsing", link)
    page = BeautifulSoup(response.content, 'html.parser')
    print("shitting", link)
    if not is_in_english(page):
        return None

    if "wikipedia.org" in link:
        return parseWikipediaPage(page)
    else:
        return parseGeneral(page, entity_name)

def crawlLinks(links: List[str], entity_name:str)->  List[tuple[str, List[str]]]:
    results = []
    for link in links[0:3]:
        result = crawlLink(link, entity_name)
        if result:
            heading, paragraphs = result
            results.append(Section(heading=heading, link=link, paragraphs=paragraphs))

    return results