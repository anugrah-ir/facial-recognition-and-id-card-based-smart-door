import os
import cv2

camera = cv2.VideoCapture(int(os.getenv('SELECTED_CAMERA')))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(os.getenv('CAMERA_RESOLUTION_WIDTH')))
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(os.getenv('CAMERA_RESOLUTION_HEIGHT')))

focus_value = int(os.getenv('FOCUS_VALUE'))

def capture_with_autofocus():
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    captured, image = camera.read()
    if not captured:
        print("There's a problem with the camera, Failed to capture image.")
        exit()
    
    return image

def capture_with_fixed_focus():
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    camera.set(cv2.CAP_PROP_FOCUS, focus_value)
    captured, image = camera.read()
    if not captured:
        print("There's a problem with the camera, Failed to capture image.")
        exit()
    
    return image