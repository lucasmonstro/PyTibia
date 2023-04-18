import numpy as np
import pyautogui
from ..typings import Task
from .baseTask import BaseTask
from .groupTaskExecutor import GroupTaskExecutor


class UsePotionGroupTask(GroupTaskExecutor):
    def __init__(self, hotkey, delayAfterComplete=0):
        super().__init__()
        self.name = 'usePotionGroup'
        self.value = hotkey
        self.tasks = self.makeTasks(hotkey, delayAfterComplete)

    # TODO: add unit tests
    # TODO: add perf
    # TODO: add typings
    def makeTasks(self, hotkey, delayAfterComplete):
        return np.array([
            UsePotionTask(hotkey, delayAfterComplete=delayAfterComplete),
        ], dtype=Task)


class UsePotionTask(BaseTask):
    def __init__(self, hotkey, delayAfterComplete=0):
        super().__init__()
        self.delayAfterComplete = delayAfterComplete
        self.name = 'usePotionTask'
        self.value = hotkey

    # TODO: add unit tests
    # TODO: add perf
    # TODO: add typings
    def do(self, context):
        pyautogui.press(self.value)
        return context