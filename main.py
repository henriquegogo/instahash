#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re, json
from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return ''

@app.route("/<hashtag>")
def hashtag(hashtag):
    text = request.args.get('text') or ''
    duration = int(request.args.get('duration')) * 1000 if request.args.get('duration') else 5000
    startdate = int(request.args.get('startdate') or 0)
    url = 'https://www.instagram.com/explore/tags/{}/'.format(hashtag)
    customization = request.args.get('customization') or ''

    response_body = requests.get(url).text
    match = re.search('>window._sharedData = (.*);<', response_body)
    json_string = match.group(1)
    timeline_object = json.loads(json_string)
    timeline_nodes = timeline_object['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    timeline_nodes = filter(lambda item: item['node']['is_video'] == False and int(item['node']['taken_at_timestamp']) > startdate, timeline_nodes)
    photos_list = map(lambda item: { 'src': item['node']['display_url'], 'text': item['node']['edge_media_to_caption']['edges'][0]['node']['text'] }, timeline_nodes)
    photos_list_json = json.dumps(photos_list)

    return render_template('show.html', list=photos_list_json, text=text, duration=duration, customization=customization)

if __name__ == "__main__":
    app.run()
