import cv2
import os
import uuid
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

# Ładowanie modelu
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)

def detect_cars(image_path):
    image = cv2.imread(image_path)
    outputs = predictor(image)
    
    # Filtruj tylko samochody (COCO class id 2 = "car")
    instances = outputs["instances"]
    car_instances = instances[instances.pred_classes == 2]

    # Wizualizacja
    v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(car_instances.to("cpu"))
    result_img = out.get_image()[:, :, ::-1]

    # Zapis przetworzonego obrazu
    filename = f'detected_{uuid.uuid4().hex}.jpg'
    output_path = os.path.join('media', filename)
    cv2.imwrite(output_path, result_img)

    return filename, len(car_instances)
