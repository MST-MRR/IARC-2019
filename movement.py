import threading
import constants as c
import time

class Movement(threading.Thread):
    def __init__(self, drone, direction, distance):
        super(Movement, self).__init__()
        self.setName("MovementThread")
        self.drone = drone
        self.direction = direction
        self.distance = distance
        self.state = c.DEFAULT
        self.stop_event = threading.Event()
        

    def get_status(self):
        return self.state

    # Called when self.Start() is called
    def run(self):
        print threading.current_thread().name, ": Starting move"
        self.state = c.ACTIVE
        self.drone.move(self.direction, self.stop_event, distance=self.distance)
        self.state = c.DEFAULT
        print threading.current_thread().name, ": Finished move"

    def cancel(self):
        self.stop_event.set()
        while self.stop_event.isSet():
            time.sleep(c.TEN_MILI)
        self.state = c.CANCELED

    # TODO
    def pause(self):
        self.state = c.WAITING
    
