from src.gameplay.typings import Context
from src.repositories.chat.core import getChatStatus
from src.utils.keyboard import press
from ...typings import Context
from .common.base import BaseTask


class EnableChatTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.name = 'enableChat'
        self.delayBeforeStart = 2
        self.delayAfterComplete = 2

    def shouldIgnore(self, context: Context) -> bool:
        (_, chatIsOn) = getChatStatus(context['screenshot'])
        shouldIgnoreTask = chatIsOn == True
        return shouldIgnoreTask

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        press('enter')
        return context

    # TODO: check if chat is off
    def did(self, _: Context) -> bool:
        return True
