import main
from modules import database, lcd
import cv2

mode = 'register'

face_feature = main.face_authentication(mode)
credential = main.id_card_authentication(mode)
    
face_data = face_feature.tobytes()
database.insert_user(face_data, credential)

success = True
main.show_result(mode, success)
key = cv2.waitKey(1) & 0xFF
if key == ord('e'):
    lcd.clear()
    cv2.destroyAllWindows()
    exit()