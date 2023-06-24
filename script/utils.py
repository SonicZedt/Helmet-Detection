import base64
import cv2
import numpy as np
from enums import ClassIdEnum

def getClassName(num:int) -> str:
    if num == 0:
        return 'Helm'
    elif num == 1:
        return 'Pengendara'
    elif num == 2:
        return 'Plat'
    else:
        return ''

def boundingBoxColor(id:ClassIdEnum) -> tuple:
    # ini (R, G, B)
    # paling kecil 0, paling gede 255
    # misal:
    # (255, 0, 0) = biru
    # (255, 255, 0) = biru campur hijau = kuning

    if id == ClassIdEnum.HELM:
        return (255, 255, 0)
    elif id == ClassIdEnum.PLAT:
        return (255, 0, 255)
    else:
        return (0, 0, 0)