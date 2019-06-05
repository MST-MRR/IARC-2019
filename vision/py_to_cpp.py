import numpy as np
import cv2

from ctypes import cdll
import ctypes
lib = cdll.LoadLibrary('./qr.so')


class Allocator:
    CFUNCTYPE = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.POINTER(ctypes.c_int))

    def __init__(self):
        self._data = None

    def __call__(self, dims, shape):
        x = np.empty(shape[:dims], np.dtype('uint32'))
        self._data = x
        return x.ctypes.data_as(ctypes.c_void_p).value

    @property
    def cfunc(self):
        return self.CFUNCTYPE(self)

    @property
    def data(self):
    	return self._data


class TS(object):
    def __init__(self, width, height, v_count=None, verticies=None):
        self.obj = lib.parameterized_init_ts(width, height, v_count, verticies) \
        	if v_count and verticies else lib.init_ts()

    def accumulate(self):
        lib.accumulate(self.obj)
        
        img = Allocator()

        lib.convert_output(self.obj, img.cfunc)

        return img.data


if __name__ == '__main__':
	# 0, 0 is in the middle of opengl, 1,1 is top right
	VCOUNT = 10
	verticies = np.array([
		-1.0, -1.0, 0.0,
		1.0, 1.0, 0.0,
		-1.0,  1.0, 0.0,
		1.0, -1.0, 0.0,
		-1.0, 0.5, 0.0,
		1.0,  0.5, 0.0,

		0.0, 1.0, 0.0,
		0.0, -1.0, 0.0,
		0.0, 1.0, 0.0,
		0.0, -1.0, 0.0,
		], dtype=np.float32)

	space = TS(1024, 768, VCOUNT, verticies.ctypes.data)
	img = space.accumulate()

	print(dict(zip(np.unique(img), np.bincount(img.flatten()))))
	print(dict(zip(*np.where(img >= 3))))

	img = np.where(img == 1, .2, 0.)
	img = np.where(img > 1, 1., img)

	print(img)

	cv2.imshow("img", img)
	cv2.waitKey(0)
