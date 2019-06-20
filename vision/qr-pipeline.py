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
    """
    PC Lines algorithm for detecting lines.

    Parameters
    ----------
    edges: image
        Values to calculate line formula from.

    Returns
    -------
    Detected slope intercept parameters [(m, b), ...].

    Description
    -----------
    Convert cartesian to line segments in Twisted and Straight space.
    Straight space consists of the parralel axes x', y'.
    Twisted space consists of the parralel axes x', -y'.

       v    T          S      
       |-y        |x         |y   
       |          |          |   
       |          |          |   
    ---|----------|----------|---u
       |-d        |0         |d  
       |          |          |   
       |          |          |   
    (T and S space attatched in the uv plane. Parralel axes separated by
    distance d along the u axis. Each parralel axis is length v.)

    The length of the axis u and v does not need to be infinite. u only
    needs to fill cover the interval [-d, d], v needs to cover the interval
    [-max(W/2, H/2), max(W/2, H/2)] (W is width of plane, H is height).

    Line formulas are calculated in slope intercept form. Local maxima
    in TS space, above a theshold, are thought to be relevant lines.

    Line formula based on space:
        ℓ: y = mx + b
        ℓS = (d, b, 1 − m),  −∞ ≤ m ≤ 0
        ℓT = (−d, −b, 1 + m),  0 ≤ m ≤ ∞.

        ℓ has one image in TS space; except when m = 0 or m = ±∞, 
        meaning, when ℓ lies in both spaces either on axis x' or y'.

        Attaching the y′ and −y′ axes results in an enclosed Mobius strip.

    Slope based on location
        ℓ is between x' & y' iff −∞ < m < 0. 
        ℓ is between x' & -y' iff 0 < m < ∞.
        ℓ is on the x' axis for vertical lines m = ±∞. 
        ℓ is on the y', -y' axis at m=0.
        ℓ is an ideal point, at infinity, at m=1.
    """
    def m(u):  # TODO
        return u

    def b(u, v):  # TODO
        return u + v

    D = 10

    IMG_WIDTH = len(edges[0])
    IMG_HEIGHT = len(edges)

    TS_WIDTH = 2 * D + 10
    TS_HEIGHT = max(IMG_WIDTH, IMG_HEIGHT)

    # 1.0 in opengl != 1 pixel !!!!

    verticies = get_ts_verticies(edges, d=D, z=0.)
    n_verticies = len(verticies) // 3 

    space = TS(TS_WIDTH, TS_HEIGHT, n_verticies, verticies.ctypes.data)

    # ensure captures all values
    accumulated = space.accumulate()

    cv2.imshow("img", np.where(accumulated > 0, .2, 0.))
    cv2.waitKey(0)

    import sys
    sys.exit()

    # (optional) take maxima above threshold.
    # (optional) take N highest maxima.
    temp_maxima = argrelextrema(accumulated, np.greater)
    maxima = zip(*temp_maxima)

    U_OFFSET = 0  ##TODO: location of u=0.
    V_OFFSET = 0  ##TODO: location of v=0.    
    
    lines = [(m(u-U_OFFSET), b(u - U_OFFSET, v - V_OFFSET)) for u, v in maxima]

    return lines


if __name__ == '__main__':
    value = '1234'

    generator = QrCode(value)

    images = [generator.img]  # [getattr(generator, section) for section in ['top_left_corner', 'top_right_corner', 'bottom_left_corner', 'bottom_right_corner']]

    for image in images:
        edges = binarize_mat(get_edges(image), threshold=.5)

        # cv2.imshow("edges", edges)
        # cv2.waitKey(0)
        
        lines = PCLines(edges)

        print(lines)
