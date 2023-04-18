import numpy as np
from src.features.gameWindow.core import getSlotFromCoordinate
from src.features.gameWindow.slot import clickSlot
from .baseTask import BaseTask


class ClickInCoordinateTask(BaseTask):
    def __init__(self, value):
        super().__init__()
        self.delayBeforeStart = 1
        self.delayAfterComplete = 0.5
        self.name = 'clickInCoordinate'
        self.value = value

    # TODO: add unit tests
    # TODO: add perf
    # TODO: add typings
    def do(self, context):
        slot = getSlotFromCoordinate(
            context['radar']['coordinate'], self.value['coordinate'])
        clickSlot(slot, context['gameWindow']['coordinate'])
        return context

    # TODO: add unit tests
    # TODO: add perf
    # TODO: add typings
    def did(self, context):
        res = context['radar']['coordinate'] == context['cavebot']['waypoints']['state']['checkInCoordinate']
        did = np.all(res) == True
        return did