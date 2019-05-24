import cv2
import numpy as np
from matplotlib import pyplot as plt

def get_edges(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.float32)/5
    dst = cv2.filter2D(gray,-1,kernel)
    lap = cv2.Laplacian(dst,cv2.CV_64F)
    cv2.imwrite('gray.jpg', lap)



