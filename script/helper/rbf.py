import cv2
import io
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dataclasses import dataclass
#from roboflow import Roboflow
#from roboflow.util.prediction import PredictionGroup

# rf = Roboflow(api_key="x9BM7fiGHoeQnSrwT67j")
# project = rf.workspace().project("helmet-ckc0w")
# model = project.version(2).model

#infer on a local image

#visualize your prediction
#model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

#infer on an image hosted elsewhere
#model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json()

class BaseRBFProp:
    def __init__(self, val):
        self.val = val

    def numpy(self):
        return [self.val]

class Cls(BaseRBFProp):
    def __init__(self, val):
        super().__init__(val)

class Xyxy(BaseRBFProp):
    def __init__(self, val):
        super().__init__(val)

class Conf(BaseRBFProp):
    def __init__(self, val):
        super().__init__(val)

class Box:
    def __init__(self, cls, xyxy:list, conf) -> None:
        self.cls = Cls(cls)
        self.xyxy = Xyxy(xyxy)
        self.conf = Conf(conf)

@dataclass
class Result:
    boxes: list[Box]

def _get_class_id(name:str) -> int:
    if name == 'helm':
        return 0
    elif name == 'motor':
        return 1
    else:
        return 2

# def detect(frame, conf=.4) -> list:
#     conf = conf * 100

#     cv2.imwrite('frame.png', frame)
#     pred_group: PredictionGroup = model.predict('frame.png', confidence=conf, overlap=30)        

#     boxes = []
#     for pred in pred_group.predictions:
#         x = pred['x']
#         y = pred['y']
#         w = pred['width']
#         h = pred['height']

#         x1 = x - w / 2
#         y1 = y - h / 2
#         x2 = x + w / 2
#         y2 = y + h / 2

#         box = Box(
#             _get_class_id(pred['class']),
#             [x1, y1, x2, y2],
#             pred['confidence']
#         )

#         boxes.append(box)

#     result = Result(boxes)
#     return [result]

def detect(frame, conf=.4):
    # curl
    conf = conf * 100

    pilframe = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buff = io.BytesIO()
    pilframe.save(buff, quality=100, format='JPEG')

    m = MultipartEncoder(fields={'file': ("imageToUpload", buff.getvalue(), "image/jpeg")})
    preds = requests.post(
        "https://detect.roboflow.com/helmet-ckc0w/2?api_key=x9BM7fiGHoeQnSrwT67j",
        data=m,
        headers={'Content-Type': m.content_type})
    preds = preds.json()['predictions']

    boxes = []
    for pred in preds:
        x = pred['x']
        y = pred['y']
        w = pred['width']
        h = pred['height']

        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2

        box = Box(
            _get_class_id(pred['class']),
            [x1, y1, x2, y2],
            pred['confidence']
        )

        boxes.append(box)

    result = Result(boxes)
    return [result]