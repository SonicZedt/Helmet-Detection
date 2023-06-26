import feed

model = None
try:
    from ultralytics import YOLO
    model = YOLO('model/best.pt')
except:
    pass


# pilih salah satu, dari gambar atau video.
# gaboleh dua-duanya sekaligus

# detect dari gambar
feed.detect_from_image(model, img_path='misc/test.png')

# detect dari video, kalo mau dari webcam tinggal ganti src=0
# atau kalo mau dari video tinggal ganti src='path/ke/video.mp4'
#feed.detect(model, src='misc/traffic.mp4')
