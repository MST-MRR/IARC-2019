

class NetworkException(Exception):
    """
    Any network or connection errors
    """
    pass


class AltitudeException(Exception):
    """
    Too low or too high altitude
    """
    pass


class ThrustException(Exception):
    """
    Too low or too high thrust
    """
    pass


class VelocityException(Exception):
    """
    Too low or too high velocity
    """
    pass


class BadArgumentException(Exception):
    """
    Caused by wrong call to function or something
    """
    pass

class EmergencyLandException(Exception):
    """
    Caused by wrong call to function or something
    """
    pass