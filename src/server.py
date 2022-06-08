import json
from flask import Flask, jsonify
from flask import Flask, send_from_directory
from flask import request
import gensim.downloader

model = gensim.downloader.load('glove-wiki-gigaword-100')

from wikipedia import crawlWikipedia

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
    data = crawlWikipedia(request.args.get("name"), request.args.get("address"))

    return json.dumps(list(map(lambda x: x.toJson(), data)))