from src.utils.core import getScreenshot
from ...typings import Context


# TODO: add unit tests
def setScreenshotMiddleware(gameContext: Context) -> Context:
    gameContext['screenshot'] = getScreenshot()
    return gameContext
