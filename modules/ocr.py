import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

def detect_and_extract_text(id_card, image):

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(id_card, config=custom_config)
    if not text:
        cv2.putText(image, 'No text detected', (10, 800), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
        return None, image
    cv2.putText(image, 'Text detected :', (10, 800), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
    cv2.putText(image, text, (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return text, image