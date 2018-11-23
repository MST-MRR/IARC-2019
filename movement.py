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
        one_pass = False
        while self.stop_event.isSet():
            time.sleep(c.SECOND)
            # In the event that the cancel is requested during the last second
            # of send_global_velocity's execution, the isSet flag will never be
            # cleared. If a second has passed (the frequency of send_global_velocity 
            # loop), then it is deduced that this is the situation, and we can break.
            if one_pass:
                break
            one_pass = True
            
        self.state = c.CANCELED

    # TODO
    def pause(self):
        self.state = c.WAITING
    
