from flask import Flask, render_template, request, Blueprint
from cropping_functions import date, amount_in_words, name, micr
from vision_api_functions import Date_extraction, Amount_extraction, Name_extraction
from micr_function import MICR_Extraction
import cv2
import numpy as np
import json
import os
from flask import jsonify

image = Blueprint('image', __name__)


# app.config["IMAGE_UPLOADS"] = "C:/Users/91974/PycharmProjects/Cheque_Digitisation/flask_requirements/"

@image.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.files:
        image2 = request.files["image"]
        image2.save(image2.filename)
        return cropping_image(image2.filename)


def cropping_image(image_path):
    all = {}
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((5, 100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    contours, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[2] * cv2.boundingRect(c)[3])

    for c in sorted_contours:
        x, y, w, h = cv2.boundingRect(c)
        date_path = date(x, y, w, h, image_path)
        micr_path = micr(x, y, w, h, image_path)
        name_path = name(x, y, w, h, image_path)
        amt_words_path = amount_in_words(x, y, w, h, image_path)
        if date_path is not None:
            all['date'] = date_path
        if micr_path is not None:
            all['micr'] = micr_path
        if name_path is not None:
            all['bearer_name'] = name_path
        if amt_words_path is not None:
            all['amount_in_words'] = amt_words_path

    return sample(all)


def sample(op):
    final_extracted_output = {'Date': Date_extraction(op['date']), 'Bearer_name': Name_extraction(op['bearer_name']),
                              'Amount_in words': Amount_extraction(op['amount_in_words'])[0],
                              'Amount': Amount_extraction(op['amount_in_words'])[1],
                              'MICR': MICR_Extraction(op['micr'])}
    os.remove(op['date'])
    os.remove(op['bearer_name'])
    os.remove(op['amount_in_words'])
    os.remove(op['micr'])

    return jsonify(final_extracted_output)

# op = upload_image()
#
# final_extracted_output = {'Date': Date_extraction(op['date']), 'Bearer_name': Name_extraction(op['bearer_name']),
#                           'Amount_in words': Amount_extraction(op['amount_in_words'])[0],
#                           'Amount': Amount_extraction(op['amount_in_words'])[1], 'MICR': MICR_Extraction(op['micr'])}
#
# with open('final_output.json', 'w') as fp:
#     json.dump(final_extracted_output, fp, indent=2)
