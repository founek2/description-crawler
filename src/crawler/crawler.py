

from typing import List, Union
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from .general import Section, parseGeneral

from .wikipedia import parseWikipediaPage

def is_in_english(soup: BeautifulSoup) -> bool:
    return soup.html and (soup.html.get("lang", "").startswith("en") or not soup.html.get("lang"))
    
def crawlLink(link: str, entity_name: str, description_prefix: Union[str, None]) -> tuple[str, List[str]]:
    session = HTMLSession()


    if "en.wikipedia.org" in link:
        page_name = link.split("/")[-1]
        link = f"https://en.wikipedia.org/w/rest.php/v1/page/{page_name}/html"
        print("crawling", link)
        response = session.get(link)
        page = BeautifulSoup(response.content, 'html.parser')
        if not is_in_english(page):
            return None

        return page_name.replace("_", " "), parseWikipediaPage(page)
    else:
        print("crawling", link)
        response = session.get(link)
        page = BeautifulSoup(response.content, 'html.parser')
        if not is_in_english(page):
            return None

        return parseGeneral(page, entity_name, description_prefix)

def crawlLinks(links, entity_name:str) ->  List[Section]:
    results = []
    for link, description_prefix in links:
        try:
            result = crawlLink(link, entity_name, description_prefix)
            if result and len(result[1]) > 0:
                heading, paragraphs = result

                if len(paragraphs) > 0:
                    section = Section(heading=heading, link=link, paragraphs=paragraphs)
                    results.append(section)
                    yield section
                else:
                    yield None
        except Exception as e:
            print("Crawling failed with error", e) 
            yield None

    return results

if __name__ == "__main__":
    print(crawlLink("https://en.wikivoyage.org/wiki/Prague", "Prague", "Prague (Czech: Praha) is the capital and largest city of the Czech Republic. The city's historic buildings and narrow, winding streets are testament to its"))
