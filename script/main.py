import feed
from database import Database
from ultralytics import YOLO

model = YOLO('model/best.pt')
#database = Database()

feed.detect(model, src='misc/Suasana Jalan Jatingaleh, Semarang saat jam kerja.mp4')
