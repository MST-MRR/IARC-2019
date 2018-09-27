# Wraps around 2DLine object
class Metric():
    def __init__(self, line, func, data_stream):
        self.line = line
        self.func = lambda x: eval(func)
        self.label = line.get_label()
        self.data_stream = data_stream
        self.data = []

    def get_line(self):
        return self.line

    def set_label(self, label):
        self.label = label

    def get_data_label(self):
        return self.label

    def get_func(self):
        return self.func

    def set_data_stream(self, data_stream):
        self.data_stream = data_stream

    def get_data_stream(self):
        return self.data_stream

    def push_data(self, data_point):
        self.data.append(data_point)
        return self.data

    def get_data(self):
        return self.data