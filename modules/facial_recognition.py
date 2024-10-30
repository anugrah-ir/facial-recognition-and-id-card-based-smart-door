import cv2
import face_recognition
import os

def detect_face(camera, unknown_face_path):
    while True:
        captured, photo = camera.read()
        if not captured:
            print('Failed to capture photo.')
            break

        cv2.imshow('Face Detection', photo)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        rgb_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_photo)
        if not faces:
            print('No face detected.')
            continue

        for (top, right, bottom, left) in faces:
            cropped_photo = photo[top:bottom, left:right]
            
        resized_photo = cv2.resize(cropped_photo, (1000, 1000))
        normalized_photo = cv2.normalize(resized_photo, None, 0, 255, cv2.NORM_MINMAX)

        normalized_face_rgb = cv2.cvtColor(normalized_photo, cv2.COLOR_BGR2RGB)
        face = face_recognition.face_encodings(normalized_face_rgb)
        
        if not face:
            print('Face too blurry.')
            continue

        face = face[0]
        cv2.imwrite(unknown_face_path, normalized_photo)
        cv2.destroyAllWindows()
        print('Face detected.')
        return face

def recognize_face(unknown_face, known_face_dir, data, tolerance):
    known_face_path = os.path.join(known_face_dir, data + '.jpg')
    known_face_photo = face_recognition.load_image_file(known_face_path)
    known_face = face_recognition.face_encodings(known_face_photo)
    known_face = known_face[0]

    match = face_recognition.compare_faces([known_face], unknown_face, tolerance=tolerance)

    return match, known_face_path
