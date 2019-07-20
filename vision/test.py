from pyzbar.pyzbar import decode
import cv2
import numpy as np

from generator.QrCode import QrCode


def barcodeReader(image, bgr):
    gray_img = image #cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    print("Barcodes:", barcodes)

    for decodedObject in barcodes:
        points = decodedObject.polygon

        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

    for bc in barcodes:
        cv2.putText(img, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    bgr, 2)

        return "Barcode: {} - Type: {}".format(bc.data.decode("utf-8"), bc.type)





value = '1234'

generator = QrCode(value)

img = getattr(generator, 'bottom_right_corner')  # generator.img



row, col= img.shape[:2]
bottom= img[row-2:row, 0:col]
mean= cv2.mean(bottom)[0]

bordersize=30
img=cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[mean,mean,mean])



img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

barcode = barcodeReader(img, (8, 70, 208))

print(barcode)

cv2.imshow('Barcode reader', img)
cv2.waitKey(0)
