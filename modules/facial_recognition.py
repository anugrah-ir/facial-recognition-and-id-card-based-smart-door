import cv2
import face_recognition
import os

face_recognition_tolerance = float(os.getenv('FACE_RECOGNITION_TOLERANCE'))

def detect_face(proccessed_image, original_image):
    proccessed_image = cv2.cvtColor(proccessed_image, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(proccessed_image)
    if len(faces) == 0:
        cv2.putText(original_image, 'No face detected', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
        return None, original_image
    
    if len(faces) > 1:
        cv2.putText(original_image, 'More than one face detected', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 3)
        return None, original_image
    
    cv2.putText(original_image, 'Face detected', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
    
    for (top, right, bottom, left) in faces:
        cropped_image = proccessed_image[top:bottom, left:right]
        cv2.rectangle(original_image, (left, top), (right, bottom), (0, 255, 0), 2)

    resized_image = cv2.resize(cropped_image, (640, 640))
    
    return resized_image, original_image

def extract_feature(face_image, original_image):
    face_features = face_recognition.face_encodings(face_image)
        
    if len(face_features) == 0:
        cv2.putText(original_image, 'Face too blurry', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 3)
        return None, original_image
    
    face_feature = face_features[0]
    return face_feature, original_image

def recognize_face(unknown_face, known_face):

    match = face_recognition.compare_faces([known_face], unknown_face, tolerance=face_recognition_tolerance)

    return match[0]