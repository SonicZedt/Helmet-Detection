import json

config = json.load(open('config.json'))

conf = config['conf']

class Library:
    tesseract_path = config['libraries']['tesseract.path']

class Map:
    location = config['map']['location']

class Resolution:
    h = config['resolution']['height']
    w = config['resolution']['width']