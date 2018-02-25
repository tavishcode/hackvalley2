#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import Flask, jsonify, request

application = Flask(__name__)
import os

# from emojiconv import object_emoji

subscription_key = os.environ.get('SUBKEY')
cv_sub_key = os.environ.get('CVSUBKEY')
if subscription_key is None or cv_sub_key is None:
    from apikeys import *
assert cv_sub_key
assert subscription_key
emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze"

# temp static
# TODO use ML
face_emoji = {
    "anger": ['😠', '😤', '😡', '👿'],
    "contempt": ['😇', '☺'],
    "disgust": ['😒', '😣', '😖'],
    "fear": ['😥', '😰', '😱'],
    "happiness": ['😁', '😀', '😂', '😄', '😃', '🙂'],
    # "neutral": ['😐', '😶', '😑', '🙄'],
    "sadness": ['😭', '😢', '😓', '😟', '🙁'],
    "surprise": ['😮', '😱', '😨', '😦', '😫', '😵'],
    "sunglasses": ['😎'],
    # "readingglasses": ['🤓'],
}


def get_face_emoji(analysis):
    maxE = None
    maxS = 0
    for face in analysis:
        for emotion, score in face["faceAttributes"]["emotion"].iteritems():
            if emotion == "neutral":
                glasses = face["faceAttributes"]["glasses"].lower()
                if glasses in ["sunglasses"]:
                    emotion = glasses
                    score = score / 2
                else:
                    score = score / 6
            if score > maxS and emotion in face_emoji:
                maxE = emotion
                maxS = score
    return face_emoji.get(maxE, [])


object_emoji = {
    'sandwich': ['🍔', '🥙', '🌯', '🌭'],
    'apple': ['🍏', '🍎'],
    'orange': ['🍊', '🍋'],
    # TODO fill or use database
}


def get_object_emoji(analysis):
    emoji = []
    for tag in analysis['tags']:
        emoji += object_emoji.get(tag['name'].lower(), [])
    return emoji


def get_face_analysis(image_data):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream"}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'smile,emotion,glasses',
    }
    response = requests.post(emotion_recognition_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    return response.json()


def get_object_analysis(image_data):
    headers = {'Ocp-Apim-Subscription-Key': cv_sub_key, "Content-Type": "application/octet-stream"}
    params = {
        'visualFeatures': 'Tags',
    }
    response = requests.post(vision_base_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    return response.json()


@application.route("/")
def rootpath():
    return jsonify({'error': 'Welcome to root'})


@application.route("/emoji", methods=['POST'])
def emoji():
    # check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'no uploaded files'})
    result = {}
    image = request.files['image']
    image_data = image.read()
    face_analysis = get_face_analysis(image_data)
    if face_analysis:
        result['emoji'] = get_face_emoji(face_analysis)
    else:
        object_analysis = get_object_analysis(image_data)
        result['emoji'] = get_object_emoji(object_analysis)
    if application.debug:
        if face_analysis:
            result['face_analysis'] = face_analysis
        elif object_analysis:
            result['object_analysis'] = object_analysis
    return jsonify(result)


# @application.route("/messenger_emoji", methods=['POST'])
# def emoji():
#     # check if the post request has the file part
#     if 'image' not in request.files:
#         return jsonify({'error': 'no uploaded files'})
#     result = {}
#     image = request.files['image']
#     image_data = image.read()
#     face_analysis = get_face_analysis(image_data)
#     if face_analysis:
#         result['emoji'] = get_face_emoji(face_analysis)
#     else:
#         object_analysis = get_object_analysis(image_data)
#         result['emoji'] = get_object_emoji(object_analysis)
#     if application.debug:
#         if face_analysis:
#             result['face_analysis'] = face_analysis
#         elif object_analysis:
#             result['object_analysis'] = object_analysis
#     return jsonify(result)


if __name__ == "__main__":
    application.debug = True
    application.run()
