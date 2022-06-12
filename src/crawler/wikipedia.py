from json import JSONEncoder
import json
from typing import List
from bs4 import BeautifulSoup
import re
from pyparsing import Optional
import requests
import re

def searchWiki(searchText):
    page = requests.get(f"https://en.wikipedia.org/w/index.php?search={searchText}&title=Special:Search&profile=advanced&fulltext=1&ns0=1")
    return BeautifulSoup(page.content, 'html.parser')

def location_of_first_brackets(text, offset):
    opened = 0
    foundOpeningAt = -1
    for position, char in enumerate(text[offset:], start=offset):
        if char == "(":
            opened += 1
            if foundOpeningAt == -1:
                foundOpeningAt = position
        if char == ")":
            opened -= 1
        if foundOpeningAt != -1 and opened == 0:
            return foundOpeningAt, position
    return -1,-1

def skip_first_brackets(paragraph):
    for el in paragraph:
        if el.name == "sup":
            el.extract()

    if paragraph.b == None:
        return paragraph.get_text()

    headline_len = len(paragraph.b.get_text())
    first_p = paragraph.get_text()
    open_pos, close_pos = location_of_first_brackets(first_p, offset=headline_len)
    if open_pos == -1:
        return first_p.strip()
    
    return (first_p[0:open_pos].strip() + first_p[close_pos + 1:]).strip()

def remove_square_brackets(text):
    return re.sub(r'\[[^\]]*\]', '',text)

def skip_all_brackets(text):
    opened = 0
    foundOpeningAt = -1
    for position, char in enumerate(text):
        if char == "(":
            opened += 1
            if foundOpeningAt == -1:
                foundOpeningAt = position
        if char == ")":
            opened -= 1
        if foundOpeningAt != -1 and opened == 0:
            # return foundOpeningAt, position
            return text[0:foundOpeningAt].strip() + skip_all_brackets(text[position + 1:])
    return remove_square_brackets(text)

# get URL
# page = requests.get("https://en.wikipedia.org/wiki/Main_Page")

 
# scrape webpage



def crawlWikipedia(name: str, address:str):
    print("Looking for:", address)
    link = findWikipediaPage(address)
    if not link:
        link = findWikipediaPage(name)

    return parseWikipediaPage(link)

# searchExists = soup.find("p", {"class": "mw-search-exists"})
# if searchExists.get_text(strip=True).startswith("There is a page named"):
#     return parseWikipedia(requests.get("https://en.wikipedia.org/" + searchExists.a["href"]))
def findWikipediaPage(text: str):
    print("Looking for:", text)
    soup = searchWiki(text)

    container = soup.find("div", {"class": "searchresults"})
    if not container or not container.ul:
        return None
    resultList = container.ul.contents
    el = resultList[0] 
    return requests.get("https://en.wikipedia.org/" + el.a["href"])

def parseWikipediaPage(soup: BeautifulSoup) -> tuple[str, List[str]]:
    content = soup.find(id="mw-content-text").find("div", {"class": "mw-parser-output"})
    content = content.contents

    allowed = []
    for el in content:
        #or el.has_attr("class") == "mw-empty-elt"
  
        # if (el.name != "p" and el.name != "h2") or el.name == None or len(el.get_text(strip=True)) == 0:
        #     el.extract()
        # else:
        #     print(el.name)
        if el.name == "h2":
            allowed.append(el)
        if  el.name == "p" and not el.find(id="coordinates") and el.get_text(strip=True) != "": # ignore coordinates
            allowed.append(el)

    #paragraphs = content  # filter empty and .mw-empty-elt
    # for item in content.find_all("p", {"class": "mw-empty-elt"}):
    #     paragraphs.remove(item)
    # for item in paragraphs:
    #     if len(item.get_text(strip=True)) == 0:
    #         item.extract()

    heading = soup.find(id="firstHeading").get_text()
    paragraphs = []
    for el in allowed[:2]:
        if el.name == "p":
            paragraphs.append(skip_all_brackets(el.get_text()))

    return heading, paragraphs
    # results = []
    # for i in range(limit):
    #     results.append(skip_first_brackets(paragraphs[i]))

    # return results
# find tags
 
# display tags
# headline_len = len(paragraphs[0].b.get_text())
# first_p = paragraphs[0].get_text()
# open_pos, close_pos = location_of_first_brackets(first_p, offset=headline_len)
# print(first_p[0:open_pos - 1] + first_p[close_pos + 1:])
if __name__ == "__main__":
    # print(searchWikipedia("Prague"))
    # crawlWikipedia("Prague", "Prague czechia")
    # searchWikipedia("Prague")

    # print(json.dumps(list(map(lambda x: x.toJson(), searchWikipedia("Prague")))))
    print(skip_all_brackets("Kyoto (/ˈkjoʊtoʊ/;[3] Japanese: 京都, Kyōto [kʲoꜜːto] (listen)), officially Kyoto City (京都市, Kyōto-shi, [kʲoːtoꜜɕi] (listen)), is the capital city of Kyoto Prefecture in Japan. Located in the Kansai region on the island of Honshu, Kyoto forms a part of the Keihanshin metropolitan area a"))