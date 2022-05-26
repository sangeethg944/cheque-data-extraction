import cv2
import numpy as np


# function for cropping date portion
def date(x, y, w, h, path):
    image = cv2.imread(path)
    area = float(w) * float(h)

    if area > 5000:
        if ((1550 <= x <= 1850) and (50 <= y <= 140)) and ((330 <= w <= 970) and (45 <= h <= 150)):
            if 1650 <= x <= 1690:
                x += 120
                w -= 120
            if x < 1649:
                x += 160
            if 50 <= y <= 80:
                y += 22
                h -= 22
            if h > 80:
                h -= 30
            d = image[y:y + h, x:x + w]
            d_name = "date" + "_" + str(x) + "_" + str(y) + "_" + str(w) + "_" + str(h) + ".jpg"
            cv2.imwrite(d_name, d)
            return d_name


# function for cropping MICR code portion
def micr(x, y, w, h, path):
    img = cv2.imread(path)
    area = float(w) * float(h)
    if area > 4000:
        if ((530 <= x <= 570) and (930 <= y <= 1020)) or ((1210 <= w <= 1220) and (38 <= h <= 48)):
            if w < 1100:
                w += 410

            m = img[y:y + h, x:x + w]
            m_name = "micr" + "_" + str(x) + "_" + str(y) + "_" + str(w) + "_" + str(h) + ".jpg"
            cv2.imwrite(m_name, m)
            return m_name


# function for cropping bearer name portion
def name(x, y, w, h, path):
    image = cv2.imread(path)
    area = float(w) * float(h)
    if area > 90000:
        if (x <= 40) and (y <= 275):
            x = 180
            y = 200
            w = 1700
            if h > 135:
                h = 135

            m = image[y:y + h, x:x + w]
            n_name = "name" + "_" + str(x) + "_" + str(y) + "_" + str(w) + "_" + str(h) + ".jpg"
            cv2.imwrite(n_name, m)
            return n_name


# function for cropping amount (in words and digits) portion
def amount_in_words(x, y, w, h, path):
    image = cv2.imread(path)
    area = float(w) * float(h)
    if area > 150000:
        if (x <= 40) and (y <= 300):
            x = 180
            h = 250
            y = 290
            if h > 135:
                h = 240
            if w <= 2000:
                w = 2330

            words = image[y:y + h, x:x + w]
            w_name = "amt_words" + "_" + str(x) + "_" + str(y) + "_" + str(w) + "_" + str(h) + ".jpg"
            cv2.imwrite(w_name, words)
            return w_name


# function for cropping amount in digits(only) images
def amount_in_digits(src_path_of_amt_words):
    image = cv2.imread(src_path_of_amt_words)
    x, y = 1500, 100
    w, h = image.shape[1] - 100, image.shape[0]
    digits = image[y:y + h, x:x + w]
    digits_name = "amt_digits" + "_" + str(x) + "_" + str(y) + "_" + str(w) + "_" + str(h) + ".jpg"
    cv2.imwrite(digits_name, digits)
    return digits_name
