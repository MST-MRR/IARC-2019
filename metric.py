# Wraps around 2DLine object


class Metric:
    """
    Piece of data to be tracked.

    Parameters
    ----------
    line: axis
        The animation line to plot data on
    func: string, optional A
        The function to generate values(takes variables x, y, z corresponding to data streams)
    x_stream: string, optional A
        Data stream for x variable in function
    y_stream: string, optional
        Data stream for y variable in function
    z_stream: string, optional
        Data stream for z variable in function
    xml_tag: xml element object, optional B
        The whole metric tag parsed from config to be parsed in metric
    """

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
        """
        Line getter.

        Returns
        -------
        line
            The animation line where this metrics data will be plotted
        """

        return self._line

    @property
    def get_label(self):
        """
        Label getter.

        Returns
        -------
        string
            Line label
        """

        return self._label

    @get_label.setter
    def set_label(self, label):
        """
        Label setter.

        Parameters
        ----------
        label: string
            New line label
        """

        self._label = label

    @property
    def get_func(self):
        """
        Func getter.

        Returns
        -------
        lambda
            The lambda functions that this metrics values will be generated with
        """

        return self._func

    @property
    def get_x_stream(self):
        """
        x_stream getter.

        Returns
        -------
        string
            Data stream to be used for x value in metric.
        """

        return self._x_stream

    @property
    def get_y_stream(self):
        """
        y_stream getter.

        Returns
        -------
        string
            Data stream to be used for y value in metric.
        """

        return self._y_stream

    @property
    def get_z_stream(self):
        """
        z_stream getter.

        Returns
        -------
        string
            Data stream to be used for z value in metric.
        """

        return self._z_stream

    @get_x_stream.setter
    def set_x_stream(self, stream):
        """
        x_stream setter.

        Parameters
        ----------
        stream: string
            New x_stream value
        """

        self._x_stream = stream

    @get_y_stream.setter
    def set_y_stream(self, stream):
        """
        y_stream setter.

        Parameters
        ----------
        stream: string
            New y_stream value
        """

        self._y_stream = stream

    @get_z_stream.setter
    def set_z_stream(self, stream):
        """
        z_stream setter.

        Parameters
        ----------
        stream: string
            New z_stream value
        """

        self._z_stream = stream

    @property
    def get_data(self):
        """
        Data getter.

        Returns
        -------
        list
            All previously generated data
        """

        return self._data

    @get_data.setter
    def push_data(self, data_point):
        """
        Data setter.

        Parameters
        ----------
        data_point: float
            Data to be appended to data
        """

        self._data.append(data_point)
