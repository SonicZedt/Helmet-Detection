import base64
import cv2
import numpy as np

def getClassName(num:int) -> str:
    if num == 0:
        return 'Helm'
    elif num == 1:
        return 'Pengendara'
    elif num == 2:
        return 'Plat'
    else:
        return ''

class Output:    
    def show_by_id(id:int, db):
        result = db.get_by_id(id)
        
        print(f"""
        Result for data {id}
        - Plate Number: {result[1]}
        - Location: {result[3]}
        - Date Captured: {result[4].strftime("%Y/%m/%d %H:%M:%S")}
        """)

        buffer = base64.b64decode(result[2])
        img = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), flags=1)

        cv2.imshow(str(id), img)
        cv2.waitKey(0)