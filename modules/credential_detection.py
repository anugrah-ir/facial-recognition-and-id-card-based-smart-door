import cv2
import re
from . import ocr
from . import data_extraction

def detect_credentials(camera):
    while True:
        text = ocr.detect_text(camera)
        data = data_extraction.get_key_value_pair(text)
        if not data:
            print('Text too blurry.')
            continue

        key, value = data
            
        if not key == 'NIK':
            print('No credential detected.')
            continue
        
        is_16_digit_number = re.fullmatch(r'\d{16}', value)

        if not is_16_digit_number:
            print('Credential value invalid')
            continue

        cv2.destroyAllWindows()
        return value