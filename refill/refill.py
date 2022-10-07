import pyautogui
import utils.image
import utils.core
import utils.mouse
import chat.chat
from time import sleep

npcTradeBarImg = utils.image.loadAsGrey('refill/images/npcTradeBar.png')
npcTradeOkImg = utils.image.loadAsGrey('refill/images/npcTradeOk.png')


@utils.core.cacheObjectPos
def getTradeTopPos(screenshot):
    return utils.core.locate(screenshot, npcTradeBarImg)


@utils.core.cacheObjectPos
def getTradeBottomPos(screenshot):
    (x, y, w, h) = getTradeTopPos(screenshot)
    (botX, botY, width, height) = utils.core.locate(utils.image.crop(
        screenshot, x, y, 174, len(screenshot) - y), npcTradeOkImg)
    return x, y + botY + 26, 174, 2


def findItem(screenshot, itemName):
    (tx, ty, _, _) = getTradeTopPos(screenshot)
    (bx, by, _, _) = getTradeBottomPos(screenshot)
    utils.mouse.leftClick(bx+160, by-75)
    sleep(0.2)
    utils.mouse.leftClick(bx + 16, by - 75)
    sleep(0.2)
    pyautogui.typewrite(itemName)
    sleep(0.2)
    utils.mouse.leftClick(tx + 90, ty + 75)
    sleep(0.2)


def setAmount(screenshot, amount):
    (bx, by, _, _) = getTradeBottomPos(screenshot)
    utils.mouse.leftClick(bx + 115, by - 42)
    sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    sleep(0.2)
    utils.core.press('backspace')
    pyautogui.typewrite(str(amount))


def buyItem(screenshot):
    (bx, by, _, _) = getTradeBottomPos(screenshot)
    utils.mouse.leftClick(bx + 150, by - 18)


def startTrade(screenshot):
    chat.chat.sendMessage(screenshot, 'hi')
    sleep(0.2)
    chat.chat.sendMessage(screenshot, 'trade')
    sleep(0.2)


def buyItems(screenshot, itemAndQuantity):

    startTrade(screenshot)
    screenshot = utils.image.RGBtoGray(utils.core.getScreenshot())
    for item in itemAndQuantity:
        (itemName, amount) = item
        findItem(screenshot, itemName)
        sleep(0.2)
        setAmount(screenshot, amount)
        sleep(0.2)
        buyItem(screenshot)
        sleep(0.2)
