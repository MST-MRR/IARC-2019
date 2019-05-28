import cv2
import numpy as np


def binarize_mat(img):
	"""
	Convert mat to binary based on threshold.

	Parameters
	----------
	img: mat
		OpenCV mat.

	Returns
	-------
	Mat with all values in [0, 1].
	"""

	img = np.where(img > .5, 1., 0.)

	return img


def get_ts_verticies(edges):
	"""
	Convert edge coordinates to verticies of lines in TS space.

	Parameters
	----------
	edges: mat
		OpenCV mat with edges = 1.

	Returns
	-------
	List of pairs of 3 tuples representing verticies of lines.
	"""
	u = 5
	rule = lambda x, y: ((-u, -y), (0, x), (u, y))

	print(rule(1, 1))

	# for each edge in mat, create 2 lines




if __name__ == '__main__':
	edges = cv2.imread('edges.jpg')

	get_ts_verticies(binarize_mat(edges))
