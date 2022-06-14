import re
from typing import List
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from crawler.general import uniq, uniq_links


link_blacklist = [
    # just wikipedia images
    "commons.wikimedia.org", 
    # no useful informations
    "tripadvisor.com", 
    "facebook.com",
    # takes > 20s to load
    "wikitravel.org",
    "www.pinterest.com"
    ]

def prefer_wikipedia(link_tags):
    links = [link for link in link_tags if not any(x in link.get("href") for x in link_blacklist)]
    result = []
    rest = []
    for link in links:
        if "wikipedia.org" in link.get("href") or "wikivoyage.org" in link.get("href"):
            result.append(link)
        else:
            rest.append(link)

    return result + rest

def has_link(tag):
    '''Returns True for tags with a href attribute'''
    if not (tag.name =="a" and bool(tag.get("href"))):
        return False
    if not tag.find("h3"):
        return False
        
    if "google" in tag.get("href") or "facebook.com" in tag.get("href"):
        return False
    return tag.get("href").startswith("http")

def get_description_container(tag):
    if tag.name != "span":
        return False
    return "..." in tag.get_text()

def remove_three_dots(text):
    return re.sub("\.\.\..*$", "", text).strip()

def enrich_with_description(el, depth = 4, original_link_tag = None):
    if original_link_tag == None:
        original_link_tag = el

    if depth == 0:
        return original_link_tag.get("href"), None


    description_tag = el.find(get_description_container)
    if description_tag:
        description_text = remove_three_dots(description_tag.get_text())
        if len(description_text) > 40:
            return original_link_tag.get("href"), description_text
    
    return enrich_with_description(el.parent, depth -1, original_link_tag)
    
def get_page(searchText):
    query = urllib.parse.quote_plus(searchText)
    session = HTMLSession()
    link = f"https://www.google.co.uk/search?q={query}&lr=lang_en&hl=en&cr=US"
    print("searching links", link)
    response = session.get(link)
    return BeautifulSoup(response.content, 'html.parser')

#tuple(link_href, description_text)
def searchForLinks(searchText: str)-> List[tuple[str, str]]:
    soup = get_page(searchText)
    
    just_link_tags = uniq_links(soup.find_all(has_link))
    just_link_tags = prefer_wikipedia(just_link_tags)

    enriched_links = [enrich_with_description(link_tag) for link_tag in just_link_tags]

    return enriched_links

# G_API_KEY = ""

# def searchForEntities(searchText: str) -> List[tuple[str, str, float]]:
#     query = urllib.parse.quote_plus(searchText)
#     url = f"https://kgsearch.googleapis.com/v1/entities:search?query={query}&key={G_API_KEY}&limit=5&indent=True"
#     response = requests.request("GET", url)
#     body = response.json()
#     # print("body response", body)
#     results = []
#     for item in body["itemListElement"]:
#         element = item["result"]
#         score = element["resultScore"]
#         description = element["detailedDescription"]
#         descriptionText = description["articleBody"]
#         link = description["url"]
#         results.append((link, descriptionText, score))

#     return results
    

if __name__ == "__main__":
    searchForLinks("wiki Versailles Gardens")