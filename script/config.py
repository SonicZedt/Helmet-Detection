import json

config = json.load(open('config.json'))

conf = config['conf']

class Resolution:
    h = config['resolution']['height']
    w = config['resolution']['width']