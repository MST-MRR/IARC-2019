"""
Pipeline from image of qr code to sending its value.
"""
import cv2
import numpy as np
from scipy.signal import argrelextrema

from generator.QrCode import QrCode
from normalize.edges import get_edges
from normalize.ts_converter import get_ts_verticies, binarize_mat
from accumulator.py_to_cpp import TS


def PCLines(edges):
    ##PC Lines

    # Input: Image I w/ dimensions (W, H)
    # Output: Detected lines L = {(m, b), ...}
    
    #S(u, v) = 0, for u in {-d, ... d}, v in {vmin, ... vmax}
    
    #for all x in {1...W}, y in {1...H}:
        
        #if I(x, y) is an edge:
            
            #rasterize line in S space
            
            #rasterize line in T space

    # two-segment polyline defined by three points: (−d, −y),(0, x),(d, y).
    # adjust coordinates to work w/ accumulator
    # should be n-1 lines w/ n dimension vector
    verticies = get_ts_verticies(edges, d=10, z=0.)

    vertex_count = len(verticies) // 3 
 
    # ensure verticies fit on screen or adjust screen

    space = TS(1024, 768, vertex_count, verticies.ctypes.data)

    # what does  0, 0 in this mean
    accumulated = space.accumulate()

    # out = np.where(accumulated > 0, .2, 0.)
    # cv2.imshow("img", out)
    # cv2.waitKey(0)

    # (optional) take maxima above threshold.
    # (optional) take N highest maxima.
    temp_maxima = argrelextrema(accumulated, np.greater)
    maxima = zip(*temp_maxima)
    # tune output X, Y
    """
    UV plane:
        Straight Space S: parallel axis x', y'
        Twisted Space T: parallel axis x', -y'

    Line formula based on space:
        ℓ: y = mx + b
        ℓS = (d, b, 1 − m)  −∞ ≤ m ≤ 0
        ℓT = (−d, −b, 1 + m)  0 ≤ m ≤ ∞.
    
        ℓ has one image in TS space; except when m = 0 or m = ±∞, 
        meaning, when ℓ lies in both spaces either on axis x' or y'.

        Attaching the y′ and −y′ axes results in an enclosed Mobius strip.
    
    Slope based on location
        ℓ is between x' & y' iff −∞ < m < 0. 
        ℓ is between x' & -y' iff 0 < m < ∞.
        ℓ is on the x' axis for vertical lines m = ±∞. 
        ℓ is on the y', -y' axis at m=0.
        ℓ is an ideal point, at infinity, at m=1.
    
    Sufficient plane length:
        −d ≤ u ≤ d,
        − max(W/2, H/2) ≤ v ≤ max(W/2, H/2)
    
        W, H are dimensions of the input raster image.
    
       v    T          S      
       |-y        |x         |y   
       |          |          |   
       |          |          |   
    ---|----------|----------|---u
       |-d        |0         |d  
       |          |          |   
       |          |          |   
    """
    def m(u):
        return u

    def b(u, v):
        return u + v

    lines = [(m(u), b(u, v)) for u, v in maxima]

    return lines


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
    
    lines = PCLines(edges)

    print(lines)
