from threading import Event, Thread

class TwoWayEvent:
    """
        Simplifies "message/response" kinds of events. Can be used as exactly as a
        normal event would (same method names with m, a, or r appended to end)

        Data Members
        ----------
        message: threading.Thread
            Represents the "message" (ex. an emergency landing has been requested)
        acknowledge: threading.Thread
            Represents an acknowledgement of the message, but that a response is still
            pending.
        response: threading.Thread
            Represents the "response" (ex. the drone is ready to begin emergency landing)
    """
    def __init__(self):
        self.message = Event()
        self.acknowledge = Event()
        self.response = Event()

    def is_set_m(self):
        return self.message.is_set()

    def isSet_m(self):
        return self.message.is_set()

    def set_m(self):
        self.message.set()

    def clear_m(self):
        self.message.clear()

    def wait_m(self, timeout=None):
        if timeout is not None:
            return self.message.wait(timeout)
        else:
            return self.message.wait()

    def is_set_a(self):
        return self.acknowledge.is_set()

    def set_a(self):
        self.acknowledge.set()

    def clear_a(self):
        self.acknowledge.clear()

    def wait_a(self, timeout=None):
        if timeout is not None:
            return self.acknowledge.wait(timeout)
        else:
            return self.acknowledge.wait()

    def is_set_r(self):
        return self.response.is_set()

    def set_r(self):
        self.response.set()

    def clear_r(self):
        self.response.clear()

    def wait_r(self, timeout=None):
        if timeout is not None:
            return self.response.wait(timeout)
        else:
            return self.response.wait()

