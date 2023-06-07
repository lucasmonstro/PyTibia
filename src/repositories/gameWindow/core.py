from typing import Tuple, Union
from src.shared.typings import BBox, Coordinate, GrayImage, Slot
from src.utils.core import hashit, locate
from .config import arrowsImagesHashes, gameWindowCache, images


# TODO: add unit tests
# TODO: add perf
def getLeftArrowPosition(screenshot: GrayImage) -> Union[BBox, None]:
    global gameWindowCache
    if gameWindowCache['left']['position'] is not None:
        leftArrowImage = images['arrows'][gameWindowCache['left']['arrow']]
        leftArrowImageHash = hashit(leftArrowImage)
        if arrowsImagesHashes.get(leftArrowImageHash, None) is not None:
            return gameWindowCache['left']['position']
    leftGameWindow01Position = locate(screenshot, images['arrows']['leftGameWindow01'])
    if leftGameWindow01Position is not None:
        gameWindowCache['left']['arrow'] = 'leftGameWindow01'
        gameWindowCache['left']['position'] = leftGameWindow01Position
        return leftGameWindow01Position
    leftGameWindow11Position = locate(screenshot, images['arrows']['leftGameWindow11'])
    if leftGameWindow11Position is not None:
        gameWindowCache['left']['arrow'] = 'leftGameWindow11'
        gameWindowCache['left']['position'] = leftGameWindow11Position
        return leftGameWindow11Position
    leftGameWindow10Position = locate(screenshot, images['arrows']['leftGameWindow10'])
    if leftGameWindow10Position is not None:
        gameWindowCache['left']['arrow'] = 'leftGameWindow10'
        gameWindowCache['left']['position'] = leftGameWindow10Position
        return leftGameWindow10Position
    leftGameWindow00Position = locate(screenshot, images['arrows']['leftGameWindow00'])
    if leftGameWindow00Position is not None:
        gameWindowCache['left']['arrow'] = 'leftGameWindow00'
        gameWindowCache['left']['position'] = leftGameWindow00Position
        return leftGameWindow00Position


# TODO: add unit tests
# TODO: add perf
def getRightArrowPosition(screenshot: GrayImage) -> Union[BBox, None]:
    global gameWindowCache
    if gameWindowCache['right']['position'] is not None:
        rightArrowImage = images['arrows'][gameWindowCache['right']['arrow']]
        rightArrowImageHash = hashit(rightArrowImage)
        if arrowsImagesHashes.get(rightArrowImageHash, None) is not None:
            return gameWindowCache['right']['position']
    rightGameWindow01Position = locate(screenshot, images['arrows']['rightGameWindow01'])
    if rightGameWindow01Position is not None:
        gameWindowCache['right']['arrow'] = 'rightGameWindow01'
        gameWindowCache['right']['position'] = rightGameWindow01Position
        return rightGameWindow01Position
    rightGameWindow11Position = locate(screenshot, images['arrows']['rightGameWindow11'])
    if rightGameWindow11Position is not None:
        gameWindowCache['right']['arrow'] = 'rightGameWindow11'
        gameWindowCache['right']['position'] = rightGameWindow11Position
        return rightGameWindow11Position
    rightGameWindow10Position = locate(screenshot, images['arrows']['rightGameWindow10'])
    if rightGameWindow10Position is not None:
        gameWindowCache['right']['arrow'] = 'rightGameWindow10'
        gameWindowCache['right']['position'] = rightGameWindow10Position
        return rightGameWindow10Position
    rightGameWindow00Position = locate(screenshot, images['arrows']['rightGameWindow00'])
    if rightGameWindow00Position is not None:
        gameWindowCache['right']['arrow'] = 'rightGameWindow00'
        gameWindowCache['right']['position'] = rightGameWindow00Position
        return rightGameWindow00Position


# TODO: add unit tests
# TODO: add perf
def getCoordinate(screenshot: GrayImage, _) -> Union[BBox, None]:
    global gameWindowCache
    leftArrowPosition = getLeftArrowPosition(screenshot)
    if leftArrowPosition is None:
        return None
    rightArrowPosition = getRightArrowPosition(screenshot)
    if rightArrowPosition is None:
        return None
    x = ((leftArrowPosition[0] + 7 + rightArrowPosition[0]) // 2) - 480
    y = leftArrowPosition[1] + 5
    return (x, y, 960, 704)


# TODO: add unit tests
# TODO: add perf
def getImageByCoordinate(screenshot: GrayImage, coordinate, gameWindowSize) -> GrayImage:
    return screenshot[coordinate[1]:coordinate[1] +
                     gameWindowSize[1], coordinate[0]:coordinate[0] + gameWindowSize[0]]


# TODO: add unit tests
# TODO: add perf
def getSlotFromCoordinate(currentCoordinate: Coordinate, coordinate: Coordinate) -> Union[Slot, None]:
    diffX = coordinate[0] - currentCoordinate[0]
    diffXAbs = abs(diffX)
    if diffXAbs > 7:
        return None
    diffY = coordinate[1] - currentCoordinate[1]
    diffYAbs = abs(diffY)
    if diffYAbs > 5:
        return None
    gameWindowCoordinateX = 7 + diffX
    gameWindowCoordinateY = 5 + diffY
    return gameWindowCoordinateX, gameWindowCoordinateY


# TODO: add unit tests
# TODO: add perf
def getSlotImage(gameWindowImg: GrayImage, slot: Tuple[int, int], slotWidth: int) -> GrayImage:
    xOfSlot, yOfSlot = slot
    x = xOfSlot * slotWidth
    y = yOfSlot * slotWidth
    slotImg = gameWindowImg[y:y + slotWidth, x:x + slotWidth]
    return slotImg


# TODO: add unit tests
# TODO: add perf
def isHoleOpen(gameWindowImg: GrayImage, holeOpenImg: GrayImage, coordinate: Coordinate, targetCoordinate: Coordinate) -> bool:
    slotWidth = len(gameWindowImg[1]) // 15
    slot = getSlotFromCoordinate(coordinate, targetCoordinate)
    slotImg = getSlotImage(gameWindowImg, slot, slotWidth)
    holeOpenLocation = locate(slotImg, holeOpenImg)
    isOpen = holeOpenLocation is not None
    return isOpen
