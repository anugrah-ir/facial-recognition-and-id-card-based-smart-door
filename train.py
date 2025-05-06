from dotenv import load_dotenv
import os
from ultralytics import YOLO

load_dotenv()
YOLO_model = os.getenv('YOLO_MODEL')
dataset_configuration = os.getenv('DATASET_CONFIGURATION_PATH')

model = YOLO(YOLO_model)

model.train(data=dataset_configuration, epochs=50, imgsz=640, batch=16)

results = model.val(data=dataset_configuration)
print(results)

results = model.predict(source='cropped_id_card.jpg', conf=0.25)
results.show()