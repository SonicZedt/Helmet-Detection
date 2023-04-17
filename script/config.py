import json

config = json.load(open('config.json'))

class Library:
    tesseract_path = config['libraries']['tesseract.path']

class Map:
    location = config['map']['location']

class Default:
    plate_undetected = config['default']['plate.failed']

class Database:
    connection_string = config['constr']