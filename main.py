#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re, json
from flask import Flask, render_template
app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<hashtag>")
def hashtag(hashtag):
    url = 'https://www.instagram.com/explore/tags/{}/'.format(hashtag)
    response_body = requests.get(url).text
    match = re.search('>window._sharedData = (.*);<', response_body)
    json_string = match.group(1)
    timeline_object = json.loads(json_string)
    timeline_nodes = timeline_object['entry_data']['TagPage'][0]['tag']['media']['nodes']
    photos_list = map(lambda item: { 'src': item['display_src'], 'text': item['caption'] }, timeline_nodes)
    photos_list_json = json.dumps(photos_list)

    print(photos_list_json)
    return render_template('index.html', list=photos_list_json)

if __name__ == "__main__":
    app.run()
