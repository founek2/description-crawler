import json
from flask import Flask, jsonify
from flask import Flask, send_from_directory
from flask import request
from crawler import crawlLink
from google_search import searchForLinks
from steller import get_place_by_id

app = Flask(__name__)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route('/')
def hello_world():
    return send_from_directory("static", "index.html")

# @app.route('/search')
# def search():
#     textToSearch = request.args.get("text")

    # return json.dumps(list(map(lambda x: x.toJson(), searchWikipedia(textToSearch))))

@app.route('/crawl')
def crawl():
    id = request.args.get("id")
    place = get_place_by_id(id)
    links = searchForLinks(place["data"]["address"])
    print("links", links)
    data = crawlLink(links[0])
    return json.dumps(list(map(lambda x: x.toJson(), data)))