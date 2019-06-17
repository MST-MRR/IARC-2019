"""
Pipeline from image of qr code to sending its value.
"""
import cv2
import numpy as np
from generator.QrCode import QrCode
from normalize.edges import get_edges
from normalize.ts_converter import get_ts_verticies, binarize_mat
from accumulator.py_to_cpp import TS


if __name__ == '__main__':
    value = '1234'

    generator = QrCode(value)

    # switch to each corners
    image = generator.img

    # cv2.imshow("qr", image)
    # cv2.waitKey(0)

    edges = binarize_mat(get_edges(image), threshold=.5)

    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    verticies = get_ts_verticies(edges, u=10, z=0.)

    VCOUNT = len(verticies) // 3
 
    space = TS(1024, 768, VCOUNT, verticies.ctypes.data)
    img = space.accumulate()

    img = np.where(img > 0, .2, 0.)

    cv2.imshow("img", img)
    cv2.waitKey(0)
