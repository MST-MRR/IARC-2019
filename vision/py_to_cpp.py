from ctypes import cdll
lib = cdll.LoadLibrary('./qr.so')


class TS(object):
    def __init__(self, v_count=None, verticies=None):
        self.obj = lib.parameterized_init_ts(v_count, verticies) \
        	if v_count and verticies else lib.init_ts()

    def accumulate(self):
        lib.accumulate(self.obj)


if __name__ == '__main__':
	# currently cannot convert parameterized input correctly
	space = TS()
	space.accumulate()
