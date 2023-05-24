import feed
from utils import Output
from database import Database

model = None
try:
    from ultralytics import YOLO
    model = YOLO('model/best.pt')
except:
    pass

database = Database()

#feed.detect_from_image(model, database, 'misc/test.png')
feed.detect(model, None, 'misc/traffic.mp4')

#Output.show_by_id(2, database)
