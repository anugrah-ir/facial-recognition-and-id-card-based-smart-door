import cv2
import pytesseract
from PIL import Image

def detect_text(camera):
    while True:
        captured, photo = camera.read()
        if not captured:
            print('Failed to capture photo.')
            break

        cv2.imshow('Text Detection', photo)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        grayscaled_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        _, threshold_photo = cv2.threshold(grayscaled_photo, 150, 255, cv2.THRESH_BINARY_INV)

        threshold_photo_image = Image.fromarray(threshold_photo)
        text = pytesseract.image_to_string(threshold_photo_image)

        if not text:
            print('No text detected.')
            continue

        return text