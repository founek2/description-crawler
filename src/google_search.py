import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

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
    response = session.get(f"https://www.google.co.uk/search?q={query}&hl=en")
    return BeautifulSoup(response.content, 'html.parser')

def searchForLinks(searchText: str)-> str:
    soup = get_page(searchText)
    
    just_links = soup.find_all(has_link)
    return [tag.get("href") for tag in just_links if tag.get("href").startswith("http")]

    