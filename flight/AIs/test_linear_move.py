from .ai_base import AIBase
from .. import constants as c
from ... import config

HOVER_DURATION = 5
MOVE_DURATION = 5


class TestLinearMove(AIBase):
    def start(self):
        self._controller.add_takeoff_task(config.DEFAULT_ALTITUDE)
        self._controller.add_hover_task(
            config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
        self._controller.add_linear_movement_task(c.Directions.FORWARD, MOVE_DURATION)
        self._controller.add_hover_task(
            config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
        self._controller.add_land_task()
        self._controller.add_exit_task()
