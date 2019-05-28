import cv2
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ts_converter.py


if __name__ == '__main__':
	size = 512

	x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
	d = np.sqrt(x**2 + y**2)
	sigma, mu = 1.0, 0.0
	gaussian = np.exp(-((d - mu)**2 / (2.0 * sigma**2)))

	img = binarize_mat(gaussian)

	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()