from typing import List
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from crawler.general import uniq

def has_link(tag):
    '''Returns True for tags with a href attribute'''
    if not (tag.name =="a" and bool(tag.get("href"))):
        return False
    if not tag.find("h3"):
        return False
        
    if "google" in tag.get("href") or "facebook.com" in tag.get("href"):
        return False
    return True

def get_page(searchText):
    query = urllib.parse.quote_plus(searchText)
    session = HTMLSession()
    link = f"https://www.google.co.uk/search?q={query}&lr=lang_en&hl=en&cr=US"
    print("searching links", link)
    response = session.get(link)
    return BeautifulSoup(response.content, 'html.parser')

def searchForLinks(searchText: str)-> str:
    soup = get_page(searchText)
    
    just_links = soup.find_all(has_link)
    return uniq([tag.get("href") for tag in just_links if tag.get("href").startswith("http")])

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
    

    
