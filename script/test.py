import feed
from ultralytics import YOLO

model = YOLO('model/best.pt')
feed.detect_from_image(model, img_path='misc/test.png')


# from helper import rbf
# import cv2

# img = cv2.imread('misc/test.png')
# rbf.detect(img)