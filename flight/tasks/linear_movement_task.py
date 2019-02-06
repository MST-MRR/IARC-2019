from task_base import TaskBase

class LinearMovementTask(TaskBase):
    """A task that moves the drone along an axis."""

    def __init__(self, drone, direction, duration):
        """Initialize a task for moving along an axis.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The drone being controlled.
        direction : Directions.{UP, DOWN, LEFT, RIGHT, FORWARD, BACK}
            The direction to travel in.
        duration : float
            How many seconds to travel for.
        """
        super(LinearMovementTask, self).__init__(drone)
        # TODO

    def perform(self):
        # TODO
        return True
