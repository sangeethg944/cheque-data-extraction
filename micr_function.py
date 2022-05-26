from skimage.segmentation import clear_border
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time
import os
from configs import *

# function for obtaining the ROIs and it's corresponding locations

def extract_digits_and_symbols(image, charCnts, minW=5, minH=15):
    # grab the internal Python iterator for the list of character
    # contours, then  initialize the character ROI and location
    # lists, respectively
    charIter = charCnts.__iter__()
    rois = []
    locs = []
    # keep looping over the character contours until we reach the end
    # of the list
    while True:
        try:
            # grab the next character contour from the list, compute
            # its bounding box, and initialize the ROI
            c = next(charIter)
            (cX, cY, cW, cH) = cv2.boundingRect(c)
            roi = None
            # check to see if the width and height are sufficiently
            # large, indicating that we have found a digit
            if cW >= minW and cH >= minH:
                # extract the ROI
                roi = image[cY:cY + cH, cX:cX + cW]
                rois.append(roi)
                locs.append((cX, cY, cX + cW, cY + cH))
            # otherwise, we are examining one of the special symbols
            else:
                parts = [c, next(charIter), next(charIter)]
                (sXA, sYA, sXB, sYB) = (np.inf, np.inf, -np.inf,
                                        -np.inf)
                # loop over the parts
                for p in parts:
                    # compute the bounding box for the part, then
                    # update our bookkeeping variables
                    (pX, pY, pW, pH) = cv2.boundingRect(p)
                    sXA = min(sXA, pX)
                    sYA = min(sYA, pY)
                    sXB = max(sXB, pX + pW)
                    sYB = max(sYB, pY + pH)
                # extract the ROI
                roi = image[sYA:sYB, sXA:sXB]
                rois.append(roi)
                locs.append((sXA, sYA, sXB, sYB))
        # we have reached the end of the iterator; gracefully break
        # from the loop
        except StopIteration:
            break
    # return a tuple of the ROIs and locations
    return (rois, locs)


# Initialising the numbers and symbol representations
charNames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "T", "U", "A", "D"]

# Path to the reference image
ref = cv2.imread(micr_reference_path)

# Preprocessing the reference image
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV |
                    cv2.THRESH_OTSU)[1]

# Contour Detection in reference image
refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
                           cv2.CHAIN_APPROX_SIMPLE)
refCnts = imutils.grab_contours(refCnts)
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]

(refROIs, refLocs) = extract_digits_and_symbols(ref, refCnts, minW=10, minH=20)
chars = {}

for (name, roi) in zip(charNames, refROIs):
    roi = cv2.resize(roi, (36, 36))
    chars[name] = roi


def MICR_Extraction(micr_image):
    image_path = micr_image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    image_cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_cnts = imutils.grab_contours(image_cnts)
    image_cnts = contours.sort_contours(image_cnts, method="left-to-right")[0]

    (image_rois, image_locs) = extract_digits_and_symbols(thresh, image_cnts, minW=10, minH=20)

    groupOutput = []
    # all = []
    for roi in image_rois:
        scores = []
        roi = cv2.resize(roi, (36, 36))
        for charName in charNames:
            result = cv2.matchTemplate(roi, chars[charName], cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)
        groupOutput.append(charNames[np.argmax(scores)])
    f = "".join(groupOutput)
    return f
