

from typing import List
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from crawler.general import Section, parseGeneral

from .wikipedia import parseWikipediaPage

def is_in_english(soup: BeautifulSoup) -> bool:
    return soup.html and (soup.html.get("lang", "").startswith("en") or not soup.html.get("lang"))
    
def crawlLink(link: str, entity_name: str) -> tuple[str, List[str]]:
    print("crawling", link)
    session = HTMLSession()
    response = session.get(link)

    page = BeautifulSoup(response.content, 'html.parser')
    if not is_in_english(page):
        return None

    if "wikipedia.org" in link:
        return parseWikipediaPage(page)
    else:
        return parseGeneral(page, entity_name)

def crawlLinks(links: List[str], entity_name:str) ->  List[Section]:
    results = []
    for link in links:
        try:
            result = crawlLink(link, entity_name)
            if result:
                heading, paragraphs = result
                if len(paragraphs) > 0:
                    section = Section(heading=heading, link=link, paragraphs=paragraphs)
                    results.append(section)
                    yield section
                else:
                    yield None
        except:
            print("Crawling failed with error")
            yield None

    return results