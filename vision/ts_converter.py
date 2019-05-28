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
	Mat with all values in [0, 1]
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

	# for each edge in mat, create 2 lines



if __name__ == '__main__':
	x, y = np.meshgrid(np.linspace(-1,1,512), np.linspace(-1,1,512))
	d = np.sqrt(x*x+y*y)
	sigma, mu = 1.0, 0.0
	gradient = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )

	img = binarize_mat(gradient)

	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	"""
	edges = cv2.imread('edges.png')

	edges = binarize_mat(edges)

	get_ts_verticies(edges)
	"""