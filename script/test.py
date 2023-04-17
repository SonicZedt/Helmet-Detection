import cv2
import feed
from database import Database
from ultralytics import YOLO

model = YOLO('model/best.pt')
#database = Database()
img = cv2.imread('misc/test8.png')

d = feed.Detect(model, img)

def detect(foo, col:tuple):
    if not foo:
        return

    for i in range(len(foo)):
        # unpack result
        box = foo[i]
        id = box.cls.numpy()[0]
        conf = box.conf.numpy()[0]
        bb = box.xyxy.numpy()[0]

        # draw rectangle on frame
        cv2.rectangle(
            img,
            (int(bb[0]), int(bb[1])),   # top left coordinate
            (int(bb[2]), int(bb[3])),   # bottom right coordinate
            col,
            2
        )

        # write label on frame
        cv2.putText(
            img, 
            f"{str(round(conf * 100, 2))}%",
            (int(bb[0]), int(bb[1]) - 10),
            cv2.FONT_HERSHEY_COMPLEX,
            .51,
            (255, 255, 255),
            1
        )


detect(d.pengendara_results, (255, 255, 0))
detect(d.helm_results, (0, 255, 255))
detect(d.plat_results ,(0, 255, 0))

cv2.imshow('frame', img)
cv2.waitKey(0)