# Wraps around 2DLine object


class Metric:
    def __init__(self, line, func, data_stream):
        self._line = line

        self._label = line.get_label()

        self._func = lambda x: eval(func)

        self._data_stream = data_stream

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
    def get_data_stream(self):
        return self._data_stream

    @get_data_stream.setter
    def set_data_stream(self, data_stream):
        self._data_stream = data_stream

    @property
    def get_data(self):
        return self._data

    @get_data.setter
    def push_data(self, data_point):
        self._data.append(data_point)
        return self._data
