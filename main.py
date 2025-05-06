from dotenv import load_dotenv
load_dotenv()

import cv2
import os
import numpy as np
import time

from modules import facial_recognition, card_detection, ocr, data_extraction, camera, database, solenoid, lcd, pre_processing

background = cv2.imread('background.jpg')

window_name = "SMART DOOR"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def show_output(mode, step, image):
    if mode == 'authentication':
        lcd.show_text('AUTHENTICATION', 0)
        cv2.putText(image, 'AUTHENTICATION', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    elif mode == 'register':
        lcd.show_text('REGISTER', 0)
        cv2.putText(image, 'REGISTER', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    if step == 'face':
        lcd.show_text('SHOW YOUR FACE', 1)
        cv2.putText(image, 'SHOW YOUR FACE', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    elif step == 'card':
        lcd.show_text('SHOW YOUR CARD', 1)
        cv2.putText(image, 'SHOW YOUR CARD', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    cv2.imshow(window_name, image)
    return

def show_result(mode, success):
    image = cv2.imread('background.jpg')
    if mode == 'authentication':
        if success:
            cv2.putText(image, 'DOOR UNLOCKED', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.putText(image, 'PRESS L TO LOCK', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        elif not success:
            cv2.putText(image, 'IDENTITY INVALID', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
            cv2.putText(image, 'PRESS R TO RETRY', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    elif mode == 'register':
        cv2.putText(image, 'REGISTER SUCCESS', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.putText(image, 'PRESS E TO EXIT', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    cv2.imshow(window_name, image)
    return

def show_stat(face_feature, match, credential, credential_found_in_database):
    match_any_face_in_database = False
    total_face_match = 0
    face_match_list = []
    users = database.get_all_users()
    for user in users:
        known_face = np.frombuffer(user[1], dtype=np.float64)
        match = facial_recognition.recognize_face(face_feature, known_face)
        if match:
            face_match_list.append(user[2])
            match_any_face_in_database = True
            total_face_match += 1
            break
    print(f"""
            --- TEST RESULT ---
          
            1. face
            face match credential = {match}
            face match any other face in database = {match_any_face_in_database}
            number of face match in database = {total_face_match}
            list of crential with matched face = {face_match_list}

            2. card
            detected credential = {credential}
            credential found = {credential_found_in_database}
          """)

def face_authentication(mode):
    step = 'face'
    while True:

        image = camera.capture_with_autofocus()

        proccessed_image = pre_processing.pre_process_face(image)

        face_image, image = facial_recognition.detect_face(proccessed_image, image)
        if face_image is None:
            show_output(mode, step, image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                lcd.clear()
                cv2.destroyAllWindows()
                return None
            continue

        face_feature, image = facial_recognition.extract_feature(face_image, image)
        if face_feature is None:
            show_output(mode, step, image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                lcd.clear()
                cv2.destroyAllWindows()
                return None
            continue
        
        lcd.clear()
        cv2.destroyAllWindows()
        return face_feature

def id_card_authentication(mode):
    step = 'card'
    while True:

        image = camera.capture_with_fixed_focus()

        original_image = image.copy()

        id_card_image, image = card_detection.detect_card(image)
        if id_card_image is None:
            show_output(mode, step, image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                lcd.clear()
                cv2.destroyAllWindows()
                return None
            continue

        text, image = ocr.detect_and_extract_text(id_card_image, original_image)
        if text is None:
            show_output(mode, step, image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                lcd.clear()
                cv2.destroyAllWindows()
                return None
            continue

        credential = data_extraction.detect_and_extract_credential(text)
        if credential is None:
            show_output(mode, step, image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                lcd.clear()
                cv2.destroyAllWindows()
                return None
            continue

        lcd.clear()
        cv2.destroyAllWindows()
        return credential

def main():
    while True:
        database.create_table()
        solenoid.lock()

        # hanya untuk pengujian
        credential_found_in_database = False
        match = False

        mode = 'authentication'

        face_feature = face_authentication(mode)
        if face_feature is None:
            break

        credential = id_card_authentication(mode)
        if credential is None:
            break

        user = database.get_user_by_credential(credential)
        
        if user is None:
            show_result(mode, False)
            # hanya untuk pengujian
            show_stat(face_feature, match, credential, credential_found_in_database)
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('e'):
                    lcd.clear()
                    cv2.destroyAllWindows()
                    break
                if key == ord('r'):
                    lcd.clear()
                    cv2.destroyAllWindows()
                    main()

        # hanya untuk pengujian
        credential_found_in_database = True
            
        known_face = np.frombuffer(user[1], dtype=np.float64)

        match = facial_recognition.recognize_face(face_feature, known_face)
        if not match:
            show_result(mode, False)
            # hanya untuk pengujian
            show_stat(face_feature, match, credential, credential_found_in_database)
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('e'):
                    lcd.clear()
                    cv2.destroyAllWindows()
                    break
                if key == ord('r'):
                    lcd.clear()
                    cv2.destroyAllWindows()
                    main()
        
        solenoid.unlock()
        show_result(mode, True)

        # hanya untuk pengujian
        show_stat(face_feature, match, credential, credential_found_in_database)

        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 15:
                break
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):
                lcd.clear()
                cv2.destroyAllWindows()
                break
            if key == ord('l'):
                lcd.clear()
                cv2.destroyAllWindows()
                break
        continue

if __name__ == "__main__":
    main()