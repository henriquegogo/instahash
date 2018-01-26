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
    timeline_nodes = timeline_object['entry_data']['FeedPage'][0]['graphql']['user']['edge_web_feed_timeline']['edges']
    timeline_nodes = filter(lambda item: item['is_video'] == False and int(item['date']) > startdate, timeline_nodes)
    photos_list = map(lambda item: { 'src': item['display_src'], 'text': item['caption'] }, timeline_nodes)
    photos_list_json = json.dumps(photos_list)

    return render_template('show.html', list=photos_list_json, text=text, duration=duration, customization=customization)

if __name__ == "__main__":
    app.run()
