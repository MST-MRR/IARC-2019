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

    # adjust coordinates to work w/ accumulator
    # should be n-1 lines w/ n dimension vector
    # two-segment polyline defined by three points: (−d, −y),(0, x),(d, y).
    verticies = get_ts_verticies(edges, u=10, z=0.)

    vertex_count = len(verticies) // 3 
 
    # ensure verticies fit on screen or adjust screen

    space = TS(1024, 768, vertex_count, verticies.ctypes.data)

    # what does  0, 0 in this mean
    accumulated = space.accumulate()

    # out = np.where(accumulated > 0, .2, 0.)
    # cv2.imshow("img", out)
    # cv2.waitKey(0)

    maxima = argrelextrema(accumulated, np.greater)
    X, Y = maxima

    # Only take accumulators above threshold !

    # (optional) Find N highest maxima
    print(maxima)


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

    
    """
    # Input: Image I w/ dimensions (W, H)
    # Output: Detected lines L = {(m, b), ...}
    
    #S(u, v) = 0, for u in {-d, ... d}, v in {vmin, ... vmax}
    
    #for all x in {1...W}, y in {1...H}:
        
        #if I(x, y) is an edge:
            
            #rasterize line in S space
            
            #rasterize line in T space

    #L = []
    L = []
    #L = [(m(u), b(u, v)) for u in {-d...d} ^ v in {vmin...vmax} ^ S(u, v) is a high local max]

