import feed
from utils import Output
from database import Database
from ultralytics import YOLO

model = YOLO('model/best.pt')
database = Database()

feed.detect_from_image(model, database, 'misc/test.png')

#Output.show_by_id(2, database)
