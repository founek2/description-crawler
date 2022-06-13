
import json
from flask import abort
from analysis.distance import calc_distances
from analysis.key_words import extract_keywords
from crawler.crawler import crawlLinks
from google_search import  searchForLinks

from steller import get_place_by_id


def extract_country(address: str) -> str:
    return address.split(", ")[-1]

def extract_main_name(name: str)-> str:
    return name.split(",")[0]

def generate_response(id: str):
    for data in generate_response_data(id):
        yield json.dumps(data) + "///\n" 

def prefer_wiki(links):
    result = []
    rest = []
    for link in links:
        if "wiki" in link:
            result.append(link)
        else:
            rest.append(link)

    return result + rest

def generate_response_data(id: str):
    place = get_place_by_id(id)
    if "data" not in place:
        abort(404)

    country = extract_country(place["data"]["address"])
    name = extract_main_name(place["data"]["name"])
    searchText = "wiki " + name + " " + (country if name != country else "")
    print(f"Searching google for: {searchText}")
    
    links = prefer_wiki(searchForLinks(searchText))
    print("links", links)
    links = links[0:3]

    yield {
        "links": links,
        "place": {"id": place["id"], "data": place["data"]},
    }

    for section in crawlLinks(links, place["data"]["name"]):
        if not section:
            continue
        keywords_scored = extract_keywords(section.get_text())
        keywords = [kw[0] for kw in keywords_scored]
        distances = calc_distances(place["data"]["name"].split(" ")[0].split(".")[0], keywords)
        keywords_scored_distanced = [(kw, score, distance_with_alg) for (kw, score), distance_with_alg in zip(keywords_scored, distances)]
        section.set_keywords(keywords_scored_distanced)
        
        yield section.toJson()