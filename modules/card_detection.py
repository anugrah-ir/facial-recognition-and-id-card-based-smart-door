import os
import cv2
from ultralytics import YOLO

model = YOLO(os.getenv('YOLO_WEIGHT_PATH'))

def detect_card(image):
    original_image = image.copy()
    
    results = model(image, verbose=False)
    
    for result in results:
        boxes = result.boxes.xyxy 
        confidences = result.boxes.conf
        for box, conf in zip(boxes, confidences):
            if conf < 0.95:
                cv2.putText(image, 'ID card too blurry', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 3)
                return None, image
            else:
                x1, y1, x2, y2 = map(int, box)
                id_card = original_image[y1:y2, x1:x2]
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, 'ID card detected', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
                return id_card, image
    
    cv2.putText(image, 'No ID card detected', (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
    return None, image