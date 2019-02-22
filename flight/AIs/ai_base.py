class AIBase:
    def __init__(self, controller):
        self._controller = controller

    def start(self):
        raise NotImplementedError("Please implement the start function")

    @property
    def controller(self):
        return self._controller
