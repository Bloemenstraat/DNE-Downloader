#!/usr/bin/env python3

import requests
import argparse
import cv2
import shutil
import os
import json
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm

def jsonify():
    current = os.getcwd()

    men = [os.path.join('men', f) for f in os.listdir('./men')]
    women = [os.path.join('women', f) for f in os.listdir('./women')]

    data = {'men': men, 'women': women}
    jsonified = json.dumps(data)

    with open('pictures.json', 'w') as f:
        f.write(jsonified)
        

def get_img():
    url = 'https://this-person-does-not-exist.com'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    endpoint = soup.find(id='avatar').get('src')

    img_url = url + endpoint

    filename = endpoint[5:]

    with open(filename, 'wb') as f:
        ir = requests.get(img_url, stream=True)

        if not ir.ok:
            return

        for block in ir.iter_content(1024):
            f.write(block)

        return filename

def detect_gender(filename):
    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"

    ageProto = "age_deploy.prototxt"
    ageModel = "age_net.caffemodel"

    genderProto = os.path.join("models", "gender_deploy.prototxt")
    genderModel = os.path.join("models", "gender_net.caffemodel")

    mean_values = (78.4263377603, 87.7689143744, 114.895847746)

    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)
    blob = cv2.dnn.blobFromImage(img, 1.0, (227, 227), mean_values)
    genderNet.setInput(blob)
    genderPred = genderNet.forward()
    
    if genderPred[0][0] > genderPred[0][1]:
        folder = 'men'
    else:
        folder = 'women'

    shutil.move(filename, os.path.join(folder, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help='Number of pictures required', type=int)
    parser.add_argument('-j', '--jsonify', help='Create a json file containing file names', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(os.path.join('.', 'men')): os.makedirs(os.path.join('.', 'men'))
    if not os.path.exists(os.path.join('.', 'women')): os.makedirs(os.path.join('.', 'women'))

    try:
        n = int(args.number)
    except:
        parser.print_help()
        sys.exit(0)

    print('RETRIEVING IMAGES...')
    for i in tqdm(range(n)):
        filename = get_img()
        detect_gender(filename)
    
    if args.jsonify:
        jsonify()
        print('JSON FILE CREATED!')
