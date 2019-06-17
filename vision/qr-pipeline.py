"""
Pipeline from image of qr code to sending its value.
"""
import cv2
import numpy as np
from generator.QrCode import QrCode
from normalize.edges import get_edges
from normalize.ts_converter import get_ts_verticies, binarize_mat


if __name__ == '__main__':
	# 3. Compartmentalize qr code normalizer.
	# 4. Normalize qr code in this file.
	# 5. Put cpp into accumulator/source, put other accum stuff into accumulator/
	# 6. Run accumulator on normalized code.
	value = '1234'

	generator = QrCode(value)
	
	# switch to each corners
	image = generator.img

	# cv2.imshow("qr", image)
	# cv2.waitKey(0)
	
	edges = binarize_mat(get_edges(image), threshold=.5)

	# cv2.imshow("edges", edges)
	# cv2.waitKey(0)
	
	# TEST
	print(np.unique(edges))
	verticies = get_ts_verticies(edges)

	# unit test: plot these verticies
	print(verticies)
