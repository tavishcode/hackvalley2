#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import Flask, jsonify, request
application = Flask(__name__)
import os
subscription_key = os.environ.get('SUBKEY')
if subscription_key is None:
    from apikeys import *
assert subscription_key
emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

#temp static
# TODO use ML
emojis = {
    "anger": ['😠', '😤', '😡', '👿'],
    "contempt": ['😇', '☺'],
    "disgust": ['😒','😣','😖'],
    "fear": ['😥','😰','😱'],
    "happiness": ['😁','😀','😂','😄','😃','🙂'],
    "neutral": ['😐','😶','😑','🙄'],
    "sadness": ['😭','😢','😓','😟','🙁'],
    "surprise": ['😮','😱','😨','😦','😫','😵'],
    "sunglasses": ['😎'],
    "readingglasses": ['🤓'],
}

def getEmoji(analysis):
    maxE = None
    maxS = 0
    for face in analysis:
        for emotion, score in face["faceAttributes"]["emotion"].iteritems():
            if emotion == "neutral":
                glasses = face["faceAttributes"]["glasses"].lower()
                if glasses in ["sunglasses", "readingglasses"]:
                    emotion = glasses
                else:
                    score = score/4
            if score > maxS:
                maxE = emotion
                maxS = score
    return emojis.get(maxE, [])

@application.route("/")
def rootpath():
    return 'hello world';

@application.route("/emoji", methods=['POST'])
def emoji():
    # check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'no uploaded files'})
    image = request.files['image']
    image_data = image.read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream"}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'smile,emotion,glasses',
    }
    response = requests.post(emotion_recognition_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    emojiList = getEmoji(analysis)
    return jsonify({
        'emoji': emojiList,
		'analysis': analysis
    })

if __name__ == "__main__":
    application.debug = True
    application.run()
