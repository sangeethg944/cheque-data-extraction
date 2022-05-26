from google.cloud import vision
import os
import re
import io
import json
from flask_requirements.configs import *


def count_digits(input_string):
    count = 0
    for x in input_string:
        if x.isdigit():
            count += 1
    return count


## Date Extraction

def Date_extraction(date_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
    client = vision.ImageAnnotatorClient()

    with io.open(date_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    texts = response.text_annotations
    splitted_full_text = str(texts[0].description).split("\n")
    print(splitted_full_text)
    f = []
    for t in splitted_full_text:
        if not t.isupper():
            f.append(t)
            continue
        if '' in t:
            f.append(t)
            continue

    print(",".join(f))
    if count_digits(f[0]) >= 6:
        return f[0]


## Name Extraction

def Name_extraction(name_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
    client = vision.ImageAnnotatorClient()

    with io.open(name_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    texts = response.text_annotations
    splitted_full_text = str(texts[0].description).split("\n")

    for text in splitted_full_text:
        if "BANK LTD" not in text and text is not None:
            return text


## Amount Extraction
def Amount_extraction(amount_path):
    global w
    g = []
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
    client = vision.ImageAnnotatorClient()

    with io.open(amount_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    texts = response.text_annotations

    splitted_full_text = str(texts[0].description).split("\n")
    for text in splitted_full_text:
        f = len(str(text))
        if "BANK LTD" not in text:
            if "या धारक को" not in text:
                if "OR BEARER" not in text:
                    if f > 15:
                        w = text
                        g.append(w)

        if count_digits(text) >= 3:
            if (
                    '\u20B9' in text or ',' in text or u"\N{euro sign}" in text or '/' in text or "-" in text or " " in text) and (
                    u"\N{euro sign}" or "*" in text):
                text.replace(u"\N{euro sign}", '')
                text.replace("*", '')
                # text.replace("?", '')
                # text.replace("\?", '')
                # text.replace("F", '')
                # d = text.replace(u"\u003F", '')
                d = re.sub(r'[?F]', '', text)
                if d is not None:
                    g.append(d)
                    break
    return g
