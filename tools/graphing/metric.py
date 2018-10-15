# Wraps around 2DLine object

from math import *


class Metric:
    """
    Piece of data to be tracked.

    Parameters
    ----------
    output: Line2D(plt animation) or text(plt/ax.text)
        Where to output data
    func: string, optional A
        The function, as string, to generate values(takes variables x, y, z corresponding to data streams)
    x_stream: string, optional A
        Data from drone to serve as x variable in function
    y_stream: string, optional
        Data from drone to serve as y variable in function
    z_stream: string, optional
        Data from drone to serve as z variable in function
    xml_tag: xml element object, optional B
        The whole metric tag parsed from config to be parsed in metric
    """

    def __init__(self, output, label=None, func=None, x_stream=None, y_stream=None, z_stream=None, xml_tag=None):
        self._output = output

        try:
            self._label = output.label() if not label else label
        except AttributeError:
            self._label = None
            
        #
        # Process xml tag
        if xml_tag is not None:
            func = xml_tag.get("func")

            if not x_stream: x_stream = xml_tag.get('x_stream')
            if not y_stream: y_stream = xml_tag.get('y_stream')
            if not z_stream: z_stream = xml_tag.get('z_stream')

        #
        # Set func
        assert func is not None, "No function given to metric from xml or as argument!"

        # Func safety check
        for letter in func:
            assert letter in '.0123456789 xyz()+-*/%absintfloatsincostanh', \
                "{}: Determined to be potentially unsafe at letter '{}'.".format(func, letter)

        # Init func
        if 'x' in func:
            assert x_stream, "X in function but no x_stream!"

            if 'y' in func:
                assert y_stream, "Y in function but no y_stream!"

                if 'z' in func:
                    assert z_stream, "Z in function but no z_stream!"

                    self._func = lambda x, y, z: eval(func)
                else: self._func = lambda x, y: eval(func)
            else: self._func = lambda x: eval(func)
        else: self._func = lambda: eval(func)

        #
        # Set data streams
        possible_data_streams = [
            'altitude', 'airspeed', 'velocity_x', 'velocity_y', 'velocity_z', 'voltage', 'state', 'mode', 'armed',
            'roll', 'pitch', 'yaw', 'altitude_controller_output', 'altitude_rc_output', 'target_altitude',
            'pitch_controller_output', 'pitch_rc_output', 'target_pitch_velocity', 'roll_controller_output',
            'roll_rc_output', 'target_roll_velocity', 'yaw_controller_output', 'yaw_rc_output', 'target_yaw',
            'color_image', 'depth_image', None]

        assert x_stream in possible_data_streams, "Invalid x_stream!"
        assert y_stream in possible_data_streams, "Invalid y_stream!"
        assert z_stream in possible_data_streams, "Invalid z_stream!"

        self._x_stream = x_stream
        self._y_stream = y_stream
        self._z_stream = z_stream

        #
        # Create data storage
        self._data = []

    @property
    def output(self):
        """
        Line getter.

        Returns
        -------
        line
            The animation line where this metrics data will be plotted
        """

        return self._output

    @property
    def label(self):
        """
        Label getter.

        Returns
        -------
        string
            Line label
        """

        return self._label

    @label.setter
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
    def func(self):
        """
        Func getter.

        Returns
        -------
        lambda
            The lambda functions that this metrics values will be generated with
        """

        return self._func

    @property
    def x_stream(self):
        """
        x_stream getter.

        Returns
        -------
        string
            Data stream to be used for x value in metric.
        """

        return self._x_stream

    @property
    def y_stream(self):
        """
        y_stream getter.

        Returns
        -------
        string
            Data stream to be used for y value in metric.
        """

        return self._y_stream

    @property
    def z_stream(self):
        """
        z_stream getter.

        Returns
        -------
        string
            Data stream to be used for z value in metric.
        """

        return self._z_stream

    @x_stream.setter
    def set_x_stream(self, stream):
        """
        x_stream setter.

        Parameters
        ----------
        stream: string
            New x_stream value
        """

        self._x_stream = stream

    @y_stream.setter
    def set_y_stream(self, stream):
        """
        y_stream setter.

        Parameters
        ----------
        stream: string
            New y_stream value
        """

        self._y_stream = stream

    @z_stream.setter
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
    def data(self):
        """
        Data getter.

        Returns
        -------
        list
            All previously generated data
        """

        return self._data

    def push_data(self, data_point):
        """
        Data setter.

        Parameters
        ----------
        data_point: float
            Data to be appended to data
        """

        self._data.append(data_point)
