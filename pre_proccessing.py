import os
import face_recognition
import cv2
import random
from dotenv import load_dotenv

load_dotenv()

known_face_dir = os.getenv('KNOWN_FACE_DIR')
known_face_proccessed_dir = os.getenv('KNOWN_FACE_PROCCESSED_DIR')

for known_face_path in os.listdir(known_face_dir):    

    known_face_photo = face_recognition.load_image_file(os.path.join(known_face_dir, known_face_path))
    faces = face_recognition.face_locations(known_face_photo)

    if not faces:
            print(known_face_path, ' : No face detected')

    photo = cv2.imread(os.path.join(known_face_dir, known_face_path))
    for (top, right, bottom, left) in faces:
        cropped_photo = photo[top:bottom, left:right]
            
    resized_photo = cv2.resize(cropped_photo, (1000, 1000))
    normalized_photo = cv2.normalize(resized_photo, None, 0, 255, cv2.NORM_MINMAX)

    normalized_face_rgb = cv2.cvtColor(normalized_photo, cv2.COLOR_BGR2RGB)
    face = face_recognition.face_encodings(normalized_face_rgb)

    if not face:
        print(known_face_path, ' : Face too blurry')
    
    NIK = random.randint(10**15, 10**16 - 1)
    file_name = f"{NIK}.jpg"
    cv2.imwrite(os.path.join(known_face_proccessed_dir, file_name), normalized_photo)
    print(known_face_path, ' : Success')