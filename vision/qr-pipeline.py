"""
Pipeline from image of qr code to sending its value.
"""
import cv2
import numpy as np
from scipy.signal import argrelextrema

from generator.QrCode import QrCode
from normalize.edges import get_edges
from normalize.ts_converter import get_ts_verticies, binarize_mat, pix_to_opengl
from accumulator.py_to_cpp import TS


## Add to pipeline
from processing.crop_n_stitch import crop, stitch
from processing.read import read


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
    N_MAXIMA = 2

    IMG_WIDTH = len(edges[0])
    IMG_HEIGHT = len(edges)

    scale = 1  # width needs to be set in fragment shader also!
    TS_WIDTH = int(1024 * scale) # >=  2 * D + 10
    TS_HEIGHT = int(768 * scale) # >= max(IMG_WIDTH, IMG_HEIGHT)

    U_OFFSET = int(.5 * TS_WIDTH)
    V_OFFSET = int(.5 * TS_HEIGHT)

    D = int(.5 * TS_WIDTH) - 5
    ####
    V_SCALE = 1
    ####

    verticies = get_ts_verticies(edges, U_OFFSET, V_OFFSET, V_SCALE, D)    

    opengl_verticies = pix_to_opengl(verticies, TS_WIDTH, TS_HEIGHT)

    space = TS(TS_WIDTH, TS_HEIGHT, opengl_verticies)
    accumulated = space.accumulate()

    accumulated = accumulated.reshape((TS_HEIGHT, TS_WIDTH))

    accumulated = accumulated[::-1]

    #cv2.imshow("img", np.where(accumulated > 0, 1, 0.))
    #cv2.waitKey(0)

    ########################
    # S Space
    # ℓ : u = d/(1-m)
    # ℓ : v = b/(1-m)

    # m = -d/u + 1
    # b = dv/u

    # T Space
    # ℓ : u = -d/(1+m)
    # ℓ : v = -b/(1+m)

    # m = -d/u - 1
    # b = dv/u

    # Parametrization
    ## y = mx + b
    ## point l* has (d, b, 1-m)

    def m(u):
        # S: + 1, T: -1
        if u == 0:
            return 1 ## TODO ?
        elif u > 0: ## S
            return -D / u + 1
        else:       ## T
            return -D / u - 1

    def b(u, v):
        return D * u / v
    
    maxima = []
    for _ in range(N_MAXIMA):
        pos = np.argmax(accumulated)
        accumulated[pos // len(accumulated), pos % len(accumulated)] = -1000
        maxima.append((pos % len(accumulated), pos // len(accumulated)))

    print('Maxima:', maxima)

    lines = [(m(u-U_OFFSET), b(u - U_OFFSET, v - V_OFFSET)) for u, v in maxima]

    return lines


if __name__ == '__main__':

    #####################

    value = '1234'

    generator = QrCode(value)

    images = [generator.img]  # [getattr(generator, section) for section in ['top_left_corner', 'top_right_corner', 'bottom_left_corner', 'bottom_right_corner']]

    #####################
    """
    image = np.zeros(shape=(100, 100))

    theta = 3.1415/4
    slope = np.tan(theta)

    x1 = 10
    y1 = 10

    dx = 80

    print('Real slope:', slope)

    x2 = x1 + dx
    y2 = y1 + int(slope * dx)
    cv2.line(image, (x1, y1), (x2, y2), 1., 2)

    image = image[::-1]

    images = [image]
    """
    #####################

    for image in images:
        edges = binarize_mat(get_edges(image), threshold=.5)

        # cv2.imshow("edges", edges)
        # cv2.waitKey(0)

        lines = PCLines(edges)

        print("(m, b):", lines)

        
