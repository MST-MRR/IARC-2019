import numpy as np
import cv2

from ctypes import cdll
lib = cdll.LoadLibrary('./qr.so')


class TS(object):
    def __init__(self, v_count=None, verticies=None):
        self.obj = lib.parameterized_init_ts(v_count, verticies) \
        	if v_count and verticies else lib.init_ts()

    def accumulate(self):
        lib.accumulate(self.obj)
        addr = lib.convert_output(self.obj)
        print(addr)
 

if __name__ == '__main__':
	# currently cannot convert parameterized input correctly
	VCOUNT = 10;

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
		], dtype=np.float32)  # cpp verticies=GLfloat = 32 bit!

	space = TS(VCOUNT, verticies.ctypes.data)
	space.accumulate()
