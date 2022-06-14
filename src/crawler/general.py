from typing import List, Union
from bs4 import BeautifulSoup


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
        return {
            "heading": self.heading,
            "paragraphs": self.paragraphs,
            "link": self.link,
            "keywords": [{"kw": x[0], "score": x[1], "distance": {"score": x[2][0], "alg": x[2][1]}} for x in  self.keywords]
            }

    def get_text(self):
        return ' '.join(self.paragraphs)
    def set_keywords(self, keywords_scored_distanced):
        self.keywords = keywords_scored_distanced

def uniq(arr: list)-> list:
    seen = set()
    seen_add = seen.add
    return [x for x in arr if not (x in seen or seen_add(x))]

def uniq_links(tags: list)-> list:
    seen = set()

    return [x for x in tags if not (x.get("href") in seen or seen.add(x))]

def find_all_description_metas(tag):
    return tag.name =="meta" and (tag.get("name") == "description" or tag.get("property") == "og:description")

def find_p_by_prefix(prefix):
    def wrapper(x):
        if x.name != "p":
            return False

        return x.get_text().strip().startswith(prefix)

    return wrapper

def parseGeneral(soup: BeautifulSoup, entity_mame: str, description_prefix: Union[str, None]) -> tuple[str, List[str]]:
    # soup = BeautifulSoup(page.content, 'html.parser')
    metaTags = soup.find_all(find_all_description_metas)
    meta_descriptions = uniq([tag.get("content") for tag in metaTags])
    description = description_prefix

    if len(meta_descriptions) > 0:
        description = " ".join(meta_descriptions)

    if description_prefix:
        extended_description = soup.find(find_p_by_prefix(description_prefix))
        print("extended:", extended_description.get_text())
        if extended_description and len(extended_description.get_text()) > len(description):
            print("got longer version", description, extended_description.get_text())
            description = extended_description.get_text().strip()
        

    heading = entity_mame
    if soup.title:
        heading = soup.title.get_text()

    if not description:
        return heading, []

    return heading, [description]
