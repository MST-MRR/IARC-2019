from .ai_base import AIBase
from .. import constants as c
from ... import config

HOVER_DURATION = 10


class TestHover(AIBase):
    def start(self):
        self._controller.add_takeoff_task(config.DEFAULT_ALTITUDE)
        self._controller.add_hover_task(
            config.DEFAULT_ALTITUDE, HOVER_DURATION, c.Priorities.MEDIUM)
        self._controller.add_land_task(c.Priorities.MEDIUM)
