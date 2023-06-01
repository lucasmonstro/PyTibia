import pyautogui
from ...typings import Context
from .common.base import BaseTask


class PressLogoutKeys(BaseTask):
    # TODO: add types
    def __init__(self, keys):
        super().__init__()
        self.delayBeforeStart = 1
        self.delayAfterComplete = 1
        self.name = 'pressKeys'
        self.keys = keys

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        with pyautogui.hold('ctrl'):
            pyautogui.press(['q'])
        return context
