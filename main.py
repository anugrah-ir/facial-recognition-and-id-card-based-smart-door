import cv2
import pytesseract
import os
from dotenv import load_dotenv
from PIL import Image
from modules import facial_recognition, credential_detection

load_dotenv()
selected_camera = int(os.getenv('SELECTED_CAMERA'))
tesseract_path = os.getenv('TESSERACT_PATH')
unknown_face_path = os.getenv('UNKNOWN_FACE_PATH')
known_face_proccessed_dir = os.getenv('KNOWN_FACE_PROCCESSED_DIR')
face_recognition_tolerance = float(os.getenv('FACE_RECOGNITION_TOLERANCE'))

camera = cv2.VideoCapture(selected_camera)
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def main():
    
    face = facial_recognition.detect_face(camera, unknown_face_path)
    data = credential_detection.detect_credentials(camera)

    camera.release()

    match, known_face_path = facial_recognition.recognize_face(face, known_face_proccessed_dir, data, face_recognition_tolerance)

    if not match:
        print('Face does not match.')
    
    print('Face match : ', data)
    unknown_face = Image.open(unknown_face_path)
    known_face = Image.open(known_face_path)
    unknown_face.show()
    known_face.show()

if __name__ == "__main__":
    main()