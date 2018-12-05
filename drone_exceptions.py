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

class VelocityExceededThreshold(Exception):
    """
    Caused by velocity being too high to be considered safe.
    """
    pass

class AltitudeExceededThreshold(Exception):
    """
    Caused by altitude being too high to be considered safe.
    """
    pass

class RangefinderMalfunction(Exception):
    """
    Caused by a malfunction being detected by the rangefinder.
    """
    pass

class OpticalflowMalfunction(Exception):
    """
    Caused by a malfunction being detected in the Opticalflow sensor.
    """
    pass

class AltitudeNegativeException(Exception):
    """
    Caused by altitude being negative.
    """
    pass