# Wraps around 2DLine object


class Metric:
    def __init__(self, line, func=None, x_stream=None, y_stream=None, z_stream=None, xml_tag=None):
        self._line = line

        self._label = line.get_label()

        if xml_tag is not None:
            func = xml_tag.get("func")

            x_stream = xml_tag.get('x_stream')

            y_stream = xml_tag.get('y_stream')

            z_stream = xml_tag.get('z_stream')

        if 'z' not in func:
            if 'y' not in func:
                if 'x' not in func: self._func = lambda: eval(func)
                else: self._func = lambda x: eval(func)
            else: self._func = lambda x, y: eval(func)
        else: self._func = lambda x, y, z: eval(func)

        self._x_stream = x_stream
        self._y_stream = y_stream
        self._z_stream = z_stream

        self._data = []

    @property
    def get_line(self):
        return self._line

    @property
    def get_label(self):
        return self._label

    @get_label.setter
    def set_label(self, label):
        self._label = label

    @property
    def get_func(self):
        return self._func

    @property
    def get_x_stream(self):
        return self._x_stream

    @property
    def get_y_stream(self):
        return self._y_stream

    @property
    def get_z_stream(self):
        return self._z_stream

    @get_x_stream.setter
    def set_x_stream(self, stream):
        self._x_stream = stream

    @get_y_stream.setter
    def set_y_stream(self, stream):
        self._y_stream = stream

    @get_z_stream.setter
    def set_z_stream(self, stream):
        self._z_stream = stream

    @property
    def get_data(self):
        return self._data

    @get_data.setter
    def push_data(self, data_point):
        self._data.append(data_point)
        return self._data
