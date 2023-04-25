import cv2
import ocr
import os
import base64
from enums import ClassIdEnum, LineEdge


class Result:
    def __init__(self, res) -> None:
        self.res = res
        
    def filter_result(self, id: int) -> list:
        boxes = self.res[0].boxes
        return list(filter(lambda box: box.cls.numpy()[0] == id, boxes))

    def check_bb_in_bb(self, bb_a, bb_b, ignores: list[LineEdge] = []) -> bool:
        # check if second bounding box is in first bounding box
        inside_vertical = False
        inside_horizontal = False

        top_left_a = (int(bb_a[0]), int(bb_a[1]))
        bottom_right_a = (int(bb_a[2]), int(bb_a[3]))

        top_left_b = (int(bb_b[0]), int(bb_b[1]))
        bottom_right_b = (int(bb_b[2]), int(bb_b[3]))

        # compare x1 and x2 of bb_a and bb_b
        if ((top_left_a[0] <= top_left_b[0]) or LineEdge.LEFT in ignores) and ((bottom_right_a[0] >= bottom_right_b[1]) or LineEdge.RIGHT in ignores):
            inside_vertical = True

        if ((top_left_a[1] <= top_left_b[1]) or LineEdge.TOP in ignores) and ((bottom_right_a[1] >= bottom_right_b[1]) or LineEdge.BOTTOM in ignores):
            inside_horizontal = True

        return inside_vertical and inside_horizontal


    def helmet_in_box(self, bb_rider, helm_results):
        helmets = list(filter(lambda box: self.check_bb_in_bb(bb_rider, box.xyxy.numpy()[0], [LineEdge.TOP]), helm_results))
        
        if len(helmets) > 0:
            return helmets[0]

        return None

    def license_in_box(self, bb_rider, plat_results):
        licenses = list(filter(lambda box: self.check_bb_in_bb(bb_rider, box.xyxy.numpy()[0]), plat_results))
        
        if len(licenses) > 0:
            return licenses[0]
        
        return None

class Detect:
    def __init__(self, model, frame) -> None:
        # hasil mentah deteksi
        results = model.predict(source=frame, conf=0.75)
        #DP = results[0].numpy()
        self.res = Result(results)

    # hasil deteksi yang udah dipisahin
    @property
    def helm_results(self):
        return self.res.filter_result(ClassIdEnum.HELM)
    
    @property
    def pengendara_results(self):
        return self.res.filter_result(ClassIdEnum.PENGENDARA)
    
    @property
    def plat_results(self):
        return self.res.filter_result(ClassIdEnum.PLAT)

def detect_from_image(model, db = None, img_path = ''):
    # skip kalo gada source
    if not img_path:
        return
    
    img = cv2.imread(img_path)
    
    d = Detect(model, img)

    for i in range(len(d.pengendara_results)):
        # plat yang kebaca nanti di taro di text
        text = ''

        # di dalam results ada id/class, persentase, sama koordinat tiap ujung kotak
        box = d.pengendara_results[i]
        id = box.cls.numpy()[0]
        conf = box.conf.numpy()[0]
        bb = box.xyxy.numpy()[0]

        # cek pengendara pake helm dan ada plat atau ngga
        helmet = d.res.helmet_in_box(bb, d.helm_results)
        plate = d.res.license_in_box(bb, d.plat_results)


        # kalo pake helm, lewatin.
        if helmet:
            continue


        # kalo ada plat, catet.
        if plate:
            # fokusin ke plat, crop dari frame
            bb_plate = plate.xyxy.numpy()[0]
            plate_roi = img[int(bb_plate[1]):int(bb_plate[3]), int(bb_plate[0]):int(bb_plate[2])]

            # gambar kotak (bounding box) di plat yang terdeteksi
            cv2.rectangle(
                img,
                (int(bb_plate[0]), int(bb_plate[1])),   # top left coordinate
                (int(bb_plate[2]), int(bb_plate[3])),   # bottom right coordinate
                (0, 255, 255),
                2
            )

            # baca text di frame yg udah dipotong.
            # update nilai text yang ada di atas tadi
            text = ocr.read(plate_roi)


        # encode frame dari matrix ke base64 string trus disimpen ke database
        if db:
            _, buffer = cv2.imencode(os.path.basename(img_path), img)
            encoded_string = base64.b64encode(buffer)
            db.insert(encoded_string, text)

        # gambar kotak (bounding box) di pengendara yang terdeteksi
        cv2.rectangle(
            img,
            (int(bb[0]), int(bb[1])),   # top left coordinate
            (int(bb[2]), int(bb[3])),   # bottom right coordinate
            (255, 255, 0),
            2
        )

        # tulis persentase buat jadiin label bounding box
        cv2.putText(
            img, 
            f"{str(round(conf * 100, 2))}%",
            (int(bb[0]), int(bb[1]) - 10),
            cv2.FONT_HERSHEY_COMPLEX,
            .51,
            (255, 255, 255),
            1
        )

    cv2.imshow('feed', img)
    cv2.waitKey(0)

def detect(model, db = None, src = 0):
    """
    src = 0 >> dari webcam\n
    src = 'path/ke/video.mp4' >> dari video\n
    src = 'path/ke/gambar.png' >> dari gambar
    """

    window = cv2.VideoCapture(src)

    # buat nampilin frame
    def show(frame, key):
        cv2.imshow('frame', frame)

        # tutup feed kalau key ditekan        
        if key == ord('q'):
            window.release()
            cv2.destroyAllWindows()

    while window.isOpened():
        frame_grabbed, frame = window.read()
        key = cv2.waitKey(1)

        # skip kalo gada frame yang kebaca
        if not frame_grabbed:
            continue
        
        # lakukan pendeteksian
        d = Detect(model, frame)

        # skip kalo gada pengendara yg kedetek, tapi tetap tampilin framenya
        if not d.pengendara_results:
            show(frame, key)
            continue

        for i in range(len(d.pengendara_results)):
            # plat yang kebaca nanti di taro di text
            text = ''

            # di dalam results ada id/class, persentase, sama koordinat tiap ujung kotak
            box = d.pengendara_results[i]
            id = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            # cek pengendara pake helm dan ada plat atau ngga
            helmet = d.res.helmet_in_box(bb, d.helm_results)
            plate = d.res.license_in_box(bb, d.plat_results)


            # kalo pake helm, lewatin.
            if helmet:
                continue


            # kalo ada plat, catet.
            if plate:
                # fokusin ke plat, crop dari frame
                bb_plate = plate.xyxy.numpy()[0]
                plate_roi = frame[int(bb_plate[1]):int(bb_plate[3]), int(bb_plate[0]):int(bb_plate[2])]

                # gambar kotak (bounding box) di plat yang terdeteksi
                cv2.rectangle(
                    frame,
                    (int(bb_plate[0]), int(bb_plate[1])),   # top left coordinate
                    (int(bb_plate[2]), int(bb_plate[3])),   # bottom right coordinate
                    (0, 255, 255),
                    2
                )

                # baca text di frame yg udah dipotong.
                # update nilai text yang ada di atas tadi
                text = ocr.read(plate_roi)


            # encode frame dari matrix ke base64 string trus disimpen ke database
            if db:
                _, buffer = cv2.imencode('png', frame)
                encoded_string = base64.b64encode(buffer)
                db.insert(encoded_string, text)

            # gambar kotak (bounding box) di pengendara yang terdeteksi
            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),   # top left coordinate
                (int(bb[2]), int(bb[3])),   # bottom right coordinate
                (255, 255, 0),
                2
            )

            # tulis persentase buat jadiin label bounding box
            cv2.putText(
                frame, 
                f"{str(round(conf * 100, 2))}%",
                (int(bb[0]), int(bb[1]) - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                .51,
                (255, 255, 255),
                1
            )

            show(frame, key)
