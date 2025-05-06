import cv2
import numpy as np

def pre_process_face(image):
    normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized_image

def pre_process_id_card(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresholded, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    cleaned = cv2.medianBlur(eroded, 3)
    return cleaned