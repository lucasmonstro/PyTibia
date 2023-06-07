from src.utils.keyboard import press
from ...typings import Context
from .common.base import BaseTask


class UseHotkeyTask(BaseTask):
    def __init__(self, hotkey: str, delayAfterComplete: int = 0):
        super().__init__()
        self.name = 'useHotkey'
        self.delayAfterComplete = delayAfterComplete
        self.value = hotkey

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        press(self.value)
        return context
