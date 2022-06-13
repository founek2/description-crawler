import json
from flask import Flask, Response, abort, jsonify
from flask import Flask, send_from_directory
from flask import request
from analysis.distance import calc_distances
from analysis.key_words import extract_keywords
from crawler.crawler import crawlLinks
from google_search import searchForLinks
from steller import get_place_by_id
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route('/')
def hello_world():
    return send_from_directory("static", "index.html")

def generate_response(searchText, place):
    links = searchForLinks(searchText)[0:3]
    print("links", len(links))

    yield json.dumps({
        "links": links,
        "place": {"id": place["id"], "data": place["data"]},
    })

    for section in crawlLinks(links, place["data"]["name"]):
        if not section:
            continue
        keywords_scored = extract_keywords(section.get_text())
        keywords = [kw[0] for kw in keywords_scored]
        distances = calc_distances(place["data"]["name"].split(" ")[0].split(".")[0], keywords)
        keywords_scored_distanced = [(kw, score, distance_with_alg) for (kw, score), distance_with_alg in zip(keywords_scored, distances)]
        section.set_keywords(keywords_scored_distanced)
        
        yield json.dumps(section.toJson())

@app.route('/crawl-stream')
def crawlStream():
    id = request.args.get("id")
    place = get_place_by_id(id)
    if "data" not in place:
        abort(404)
    address = place["data"]["address"].split(", ")[-1]
    searchText = place["data"]["name"] + " " + (address if place["data"]["name"].lower() != address.lower() else "")
    print(f"Searching google for: {searchText}")

    return Response(generate_response(searchText, place), mimetype='text/csv')
    
    # print("data", data)
    # return json.dumps({
    #     "data": list(map(lambda x: x.toJson(), sections)),
    #     "links": links,
    #     "place": place,
    # })

@app.route('/crawl')
def crawl():
    id = request.args.get("id")
    place = get_place_by_id(id)
    address = place["data"]["address"].split(", ")[-1]
    searchText = place["data"]["name"] + " " + (address if place["data"]["name"].lower() != address.lower() else "")
    print(f"Searching google for: {searchText}")
    links = searchForLinks(searchText)[0:3]
    
    print("links", len(links))
    sections = []
    for section in crawlLinks(links, place["data"]["name"]):
        if not section:
            continue
        keywords_scored = extract_keywords(section.get_text())
        keywords = [kw[0] for kw in keywords_scored]
        distances = calc_distances(place["data"]["name"].split(" ")[0].split(".")[0], keywords)
        keywords_scored_distanced = [(kw, score, distance_with_alg) for (kw, score), distance_with_alg in zip(keywords_scored, distances)]
        section.set_keywords(keywords_scored_distanced)
        sections.append(section)

    
    # print("data", data)
    return json.dumps({
        "data": list(map(lambda x: x.toJson(), sections)),
        "links": links,
        "place": {"id": place["id"], "data": place["data"]},
    })