

class NetworkError(Exception):
    """
    Any network or connection errors
    """
    pass


class AltitudeError(Exception):
    """
    Too low or too high altitude
    """
    pass


class ThrustError(Exception):
    """
    Too low or too high thrust
    """
    pass


class VelocityError(Exception):
    """
    Too low or too high velocity
    """
    pass


class BadArgumentError(Exception):
    """
    Caused by wrong call to function or something
    """