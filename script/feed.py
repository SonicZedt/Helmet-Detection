import cv2
import os
import config
import utils
from helper import rbf

class Detect:
    def __init__(self, model, frame, _ = True) -> None:
        # hasil mentah deteksi
        results = rbf.detect(frame, config.conf) if _ else model.predict(source=frame, conf=config.conf)

        #DP = results[0].numpy()
        self.res = results[0].boxes

def detect_from_image(model, img_path = ''):
    print("Detecting from image...")

    # skip kalo gada source
    if not img_path:
        print("img_path is empty")
        return

    # skip juga kalo path salah
    if not os.path.exists(img_path):
        print("image is not exists")
        return

    img = cv2.imread(img_path)
    
    d = Detect(model, img)

    for i in range(len(d.res)):
        # di dalam results ada id/class, persentase, sama koordinat tiap ujung kotak
        box = d.res[i]
        id = box.cls.numpy()[0]
        conf = box.conf.numpy()[0]
        bb = box.xyxy.numpy()[0]

        # gambar kotak (bounding box) di objek yang terdeteksi
        cv2.rectangle(
            img,
            (int(bb[0]), int(bb[1])),   # top left coordinate
            (int(bb[2]), int(bb[3])),   # bottom right coordinate
            utils.boundingBoxColor(id),
            2
        )

        # tulis label persentase buat jadiin label bounding box
        cv2.putText(
            img, 
            f"{utils.getClassName(id)} | {str(round(conf * 100, 2))}%",
            (int(bb[0]), int(bb[1]) - 10),
            cv2.FONT_HERSHEY_COMPLEX,
            .51,
            utils.boundingBoxColor(id),
            1
        )

    cv2.imshow('feed', img)
    cv2.waitKey(0)

def detect(model, src = 0):
    """
    src = 0 >> dari webcam\n
    src = 'path/ke/video.mp4' >> dari video
    """

    print("Detecting from video...")

    window = cv2.VideoCapture(src)

    # buat nampilin frame
    def show(frame, key):
        cv2.imshow('frame', frame)

        # tutup feed kalau key ditekan        
        if key == ord('q'):
            window.release()
            cv2.destroyAllWindows()

    # selama window masih kebuka
    while window.isOpened():
        frame_grabbed, frame = window.read()
        key = cv2.waitKey(1)

        # skip kalo gada frame yang kebaca
        if not frame_grabbed:
            continue
        
        # lakukan pendeteksian
        d = Detect(model, frame)

        # skip kalo gada objek yg kedetek, tapi tetap tampilin framenya
        if not d.res:
            show(frame, key)
            continue

        for i in range(len(d.res)):
            # di dalam results ada id/class, persentase, sama koordinat tiap ujung kotak
            box = d.res[i]
            id = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            # gambar kotak (bounding box) di objek yang terdeteksi
            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),   # top left coordinate
                (int(bb[2]), int(bb[3])),   # bottom right coordinate
                utils.boundingBoxColor(id),
                2
            )

            # tulis label dan persentase buat jadiin label bounding box
            cv2.putText(
                frame, 
                f"{utils.getClassName(id)} | {str(round(conf * 100, 2))}%",
                (int(bb[0]), int(bb[1]) - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                .51,
                utils.boundingBoxColor(id),
                1
            )

            show(frame, key)
