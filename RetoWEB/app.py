from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
import base64
import torch
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

app = Flask(__name__)
CORS(app)

# Set up Detectron2 configuration
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8  # Set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml")
predictor = DefaultPredictor(cfg)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    img_data = base64.b64decode(data['image'])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    ingredients_count = {}

    outputs = predictor(img)
    instances = outputs["instances"].to("cpu")
    pred_classes = instances.pred_classes.numpy()
    pred_scores = instances.scores.numpy()

    metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

    for i in range(len(pred_classes)):
        class_name = metadata.thing_classes[pred_classes[i]]
        score = pred_scores[i]
        if score >= 0.8:
            if class_name in ingredients_count:
                ingredients_count[class_name] += 1
            else:
                ingredients_count[class_name] = 1
            print(f"Detected {class_name} with confidence {score}")

    return jsonify(ingredients_count)

if __name__ == '__main__':
    app.run(debug=True)