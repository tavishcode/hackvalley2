#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import Flask, jsonify, request
app = Flask(__name__)
from apikeys import *
assert subscription_key
emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"


def getEmoji(analysis):
    return ['😂', '😅']

@app.route("/")
def rootpath():
    return 'hello world';

@app.route("/emoji", methods=['POST'])
def emoji():
    # check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'no uploaded files'})
    image = request.files['image']
    # return str(image)
    image_data = image.read()#open(image.tmppath, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream"}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'smile,emotion',
    }
    response = requests.post(emotion_recognition_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    emojiList = getEmoji(analysis)
    return jsonify({
        'emoji': emojiList
    })

if __name__ == "__main__":
    app.run()
