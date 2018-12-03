import threading


class SharedLock():
    """
    A class that follows the singleton design pattern. Allows
    any thread that imports this class to get a reference to the
    lock that is to be shared across all threads.

    Data Members
    ----------
    lock: threading.Lock
        A static variable that is shared among all threads
    """
    lock = None

    def __init__(self):
        self.lock = None

    @staticmethod
    def getLock():
        if SharedLock.lock is None:
            SharedLock.lock = threading.Lock()

        return SharedLock.lock