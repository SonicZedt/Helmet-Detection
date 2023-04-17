import cv2
import pytesseract
import config

pytesseract.pytesseract.tesseract_cmd = config.Library.tesseract_path

def read(img) -> str:
    text = ''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # jalanin OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # specify bentuk struktur dan ukuran kernelnya.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # dilasi di gambar yang udah di threshold tadi
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    # nyari contours
    contours, hierarchy = cv2.findContours(
        dilation, 
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()


    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Crop text per blok yang kedetek
        cropped = im2[y:y + h, x:x + w]
                
        # extrak text dari blok

    return text
