"""
Convert points to TS space.
"""
import cv2
import numpy as np


def binarize_mat(img, threshold=.5):
    """
    Convert mat to binary based on threshold.

    Parameters
    ----------
    img: mat
    	OpenCV mat.
    threshold: float
        Threshold value.

    Returns
    -------
    Mat with all values in [0, 1].
    """

    img = np.where(img > threshold, 1., 0.)

    return img


def get_ts_verticies(edges, d=10., z=1.):
    """
    Convert edge coordinates to two-segment polyline defined by 
    three points: (−d, −y),(0, x),(d, y), for TS space.

    Parameters
    ----------
    edges: mat
    	1 channel binary OpenCV mat.
    d: float
    	Spacing between axis along u.
    z: float
    	Z value.

    Returns
    -------
    Numpy array[float32] of pairs of 3 representing verticies of lines.
    """
    z = float(z)

    rule = lambda x, y: [-d, -y, z, 0., x, z, 0., x, z, d, y, z]

    verticies = []
    for index, value in np.ndenumerate(edges):
        if value == 1:
            #x, y = index
            verticies += rule(*map(float, index))

    return np.array(verticies, dtype=np.float32)


if __name__ == '__main__':
    edges = cv2.imread('edges.jpg', 0)

    get_ts_verticies(binarize_mat(edges))
