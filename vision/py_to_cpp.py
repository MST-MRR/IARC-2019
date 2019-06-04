import numpy as np
import cv2

from ctypes import cdll
import ctypes
lib = cdll.LoadLibrary('./qr.so')

class Allocator:
    CFUNCTYPE = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_char)

    def __init__(self):
        self.allocated_arrays = []

    def __call__(self, dims, shape, dtype):
        x = np.empty(shape[:dims], np.dtype(dtype))
        self.allocated_arrays.append(x)
        return x.ctypes.data_as(ctypes.c_void_p).value

    def getcfunc(self):
        return self.CFUNCTYPE(self)

    cfunc = property(getcfunc)


class TS(object):
    def __init__(self, v_count=None, verticies=None):
        self.obj = lib.parameterized_init_ts(v_count, verticies) \
        	if v_count and verticies else lib.init_ts()

    def accumulate(self):
        lib.accumulate(self.obj)
        addr = lib.convert_output(self.obj)

        #lib.load_to_python.argtypes = [..., Allocator.CFUNCTYPE]
	
        alloc = Allocator()
        lib.load_to_python(alloc.cfunc)
        print(tuple(alloc.allocated_arrays[:3]))


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

	# does the cpp destructor get called?
	# pass window size, width parameters
