import math
from numba import njit
import numpy as np
import pathlib
import tcod
from typing import List, Tuple, Union
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from src.repositories.radar.config import walkableFloorsSqms
from src.repositories.radar.core import isCoordinateWalkable
from src.shared.typings import Coordinate, GrayImage, Slot, SlotWidth, XYCoordinate
from src.utils.core import getPixelFromCoordinate, hashitHex
from src.utils.image import loadFromRGBToGray
from src.utils.matrix import getAdjacencyMatrix, hasMatrixInsideOther
from src.wiki.creatures import creatures as wikiCreatures
from .typings import Creature, CreatureList


currentPath = pathlib.Path(__file__).parent.resolve()
resolutions = {
    720: {
        'gameWindowHeight': 352,
        'gameWindowWidth': 480,
        'slotWidth': 32,
    },
    1080: {
        'gameWindowHeight': 704,
        'gameWindowWidth': 960,
        'slotWidth': 64,
    },
}
creaturesNamesHashes = {}
for creature in wikiCreatures:
    creaturesNamesHashes[creature] = loadFromRGBToGray(
        f'{currentPath}/images/monsters/{creature}.png')


# TODO: improve performance
# TODO: add unit tests
# TODO: add perf
# TODO: add typings
def getClosestCreature(gameWindowCreatures: CreatureList, coordinate: Coordinate):
    if len(gameWindowCreatures) == 0:
        return None
    gameWindowWalkableFloorsSqms = getGameWindowWalkableFloorsSqms(
        walkableFloorsSqms[coordinate[2]], coordinate)
    adjacencyMatrix = getAdjacencyMatrix(gameWindowWalkableFloorsSqms)
    sqmsGraph = csr_matrix(adjacencyMatrix)
    playerGameWindowIndex = 82
    sqmsGraphWeights = dijkstra(
        sqmsGraph, directed=True, indices=playerGameWindowIndex, unweighted=False)
    creaturesSlots = gameWindowCreatures['slot'][:, [1, 0]]
    gameWindowWalkableFloorsSqmsCreatures = np.zeros((11, 15))
    gameWindowWalkableFloorsSqmsCreatures[creaturesSlots[:,
                                                  0], creaturesSlots[:, 1]] = 1
    creaturesIndexes = np.nonzero(
        gameWindowWalkableFloorsSqmsCreatures.flatten() == 1)[0]
    creaturesGraphWeights = np.take(sqmsGraphWeights, creaturesIndexes)
    nonTargetCreaturesIndexes = np.where(creaturesGraphWeights == np.inf)[0]
    creaturesIndexes = np.delete(creaturesIndexes, nonTargetCreaturesIndexes)
    creaturesGraphWeights = np.delete(
        creaturesGraphWeights, nonTargetCreaturesIndexes)
    if len(creaturesGraphWeights) == 0:
        return None
    creaturesDistances = np.where(
        creaturesGraphWeights == np.amin(creaturesGraphWeights))[0]
    closestCreatureGameWindowIndex = creaturesIndexes[np.random.choice(
        creaturesDistances)]
    creatureSlot = [closestCreatureGameWindowIndex %
                    15, closestCreatureGameWindowIndex // 15]
    closestCreatureIndex = np.where(
        (gameWindowCreatures['slot'] == creatureSlot).all(axis=1))[0][0]
    return gameWindowCreatures[closestCreatureIndex]


# TODO: add unit tests
# TODO: add perf
@njit(cache=True, fastmath=True)
def getCreaturesBars(gameWindowImage: GrayImage):
    imgHeight, imgWidth = gameWindowImage.shape
    for j in range(imgHeight - 3):
        i = -1
        while(i < (imgWidth - 27)):
            i += 1
            if gameWindowImage[j, i + 26] == 0:
                if gameWindowImage[j, i] == 0:
                    upperBorderIsBlack = True
                    bottomBorderIsBlack = True
                    # detecting upper/bottom black borders
                    for l in range(25):
                        if gameWindowImage[j, i + 25 - l] != 0:
                            upperBorderIsBlack = False
                            i += 25 - l
                            break
                        if gameWindowImage[j + 3, i + 25 - l] != 0:
                            bottomBorderIsBlack = False
                            i += 25 - l
                            break
                    if upperBorderIsBlack == False or bottomBorderIsBlack == False:
                        continue
                    # detecting left/right bars
                    if gameWindowImage[j + 1, i] != 0 or gameWindowImage[j + 2, i] != 0 or gameWindowImage[j + 1, i + 26] != 0 or gameWindowImage[j + 2, i + 26] != 0:
                        continue
                    yield (i, j)
                    i += 26
            else:
                i += 26


# TODO: add unit tests
# TODO: add perf
# TODO: add typings
# TODO: add name missAlignment for each creature, it avoid possible 3 calculations
# TODO: maximum creatures allowed should be equal battle list size
# TODO: Find a way to avoid 3 calculation times when comparing names since some words have a wrong location
# TODO: Whenever the last species is left, avoid loops and resolve species immediately for remaining creatures bars
def getCreatures(battleListCreatures, direction, gameWindowCoordinate: XYCoordinate, gameWindowImage: GrayImage, coordinate: Coordinate, beingAttackedCreatureCategory: str=None, walkedPixelsInSqm: int=0):
    if len(battleListCreatures) == 0:
        return np.array([], dtype=Creature)
    creaturesBars = [creatureBar for creatureBar in getCreaturesBars(gameWindowImage)]
    if len(creaturesBars) == 0:
        return np.array([], dtype=Creature)
    creatures = []
    gameWindowWidth = len(gameWindowImage[1])
    x = (len(gameWindowImage[1]) / 2) - 1
    y = (len(gameWindowImage[0]) / 2) - 1
    slotWidth = len(gameWindowImage[1]) // 15
    centersBars = np.broadcast_to([x, y], (len(creaturesBars), 2))
    absolute = np.absolute(creaturesBars - centersBars)
    power = np.power(absolute, 2)
    sum = np.sum(power, axis=1)
    sqrt = np.sqrt(sum)
    creaturesBarsSortedIndexes = np.argsort(sqrt)
    discoverTarget = beingAttackedCreatureCategory is not None
    for creatureBarSortedIndex in creaturesBarsSortedIndexes:
        nonCreaturesForCurrentBar = {}
        for battleListIndex in range(len(battleListCreatures)):
            if battleListCreatures[battleListIndex]['name'] == 'Unknown':
                creature = makeCreature(battleListCreatures[battleListIndex]['name'], 'player', creaturesBars[creatureBarSortedIndex], direction, gameWindowCoordinate, gameWindowImage, coordinate, slotWidth, discoverTarget=discoverTarget, beingAttackedCreatureCategory=beingAttackedCreatureCategory, walkedPixelsInSqm=walkedPixelsInSqm)
                if creature[2]:
                    discoverTarget = False
                creatures.append(creature)
                break
            if nonCreaturesForCurrentBar.get(battleListCreatures[battleListIndex]['name'], None) is not None:
                continue
            creatureNameImg = creaturesNamesHashes.get(battleListCreatures[battleListIndex]['name']).copy()
            (creatureBarX, creatureBarY) = creaturesBars[creatureBarSortedIndex]
            creatureBarY0 = creatureBarY - 13
            creatureBarY1 = creatureBarY0 + 11
            creatureNameImgHalfWidth = math.floor(creatureNameImg.shape[1] / 2)
            leftDiff = max(creatureNameImgHalfWidth - 13, 0)
            gapLeft = 0 if creatureBarX > leftDiff else leftDiff - creatureBarX
            gapInnerLeft = 0 if creatureNameImg.shape[1] > 27 else math.ceil((27 - creatureNameImg.shape[1]) / 2)
            rightDiff = max(creatureNameImg.shape[1] - creatureNameImgHalfWidth - 14, 0)
            gapRight = 0 if gameWindowWidth > (creatureBarX + 27 + rightDiff) else creatureBarX + 27 + rightDiff - gameWindowWidth
            gapInnerRight = 0 if creatureNameImg.shape[1] > 27 else math.floor((27 - creatureNameImg.shape[1]) / 2)
            gg = 13 + gapLeft + gapInnerLeft - gapRight - gapInnerRight
            startingX = max(0, creatureBarX - creatureNameImgHalfWidth + gg)
            endingX = min(gameWindowWidth, creatureBarX + creatureNameImgHalfWidth + gg)
            creatureWithDirtNameImg = gameWindowImage[creatureBarY0:creatureBarY1, startingX:endingX]
            if creatureNameImg.shape[1] != creatureWithDirtNameImg.shape[1]:
                creatureWithDirtNameImg = gameWindowImage[creatureBarY0:creatureBarY1, startingX:endingX + 1]
            if hasMatrixInsideOther(creatureWithDirtNameImg, creatureNameImg):
                creature = makeCreature(battleListCreatures[battleListIndex]['name'], 'monster', creaturesBars[creatureBarSortedIndex], direction, gameWindowCoordinate, gameWindowImage, coordinate, slotWidth, discoverTarget=discoverTarget, beingAttackedCreatureCategory=beingAttackedCreatureCategory, walkedPixelsInSqm=walkedPixelsInSqm)
                if creature[2]:
                    discoverTarget = False
                creatures.append(creature)
                break
            creatureNameImg2 = creaturesNamesHashes.get(battleListCreatures[battleListIndex]['name']).copy()
            creatureWithDirtNameImg2 = gameWindowImage[creatureBarY0:creatureBarY1, startingX + 1:endingX + 1]
            if creatureNameImg2.shape[1] != creatureWithDirtNameImg2.shape[1]:
                creatureNameImg2 = creatureNameImg2[:, 0:creatureNameImg2.shape[1] - 1]
            if hasMatrixInsideOther(creatureWithDirtNameImg2, creatureNameImg2):
                creature = makeCreature(battleListCreatures[battleListIndex]['name'], 'monster', creaturesBars[creatureBarSortedIndex], direction, gameWindowCoordinate, gameWindowImage, coordinate, slotWidth, discoverTarget=discoverTarget, beingAttackedCreatureCategory=beingAttackedCreatureCategory, walkedPixelsInSqm=walkedPixelsInSqm)
                if creature[2]:
                    discoverTarget = False
                creatures.append(creature)
                break
            creatureWithDirtNameImg3 = gameWindowImage[creatureBarY0:creatureBarY1, startingX:endingX - 1]
            creatureNameImg3 = creaturesNamesHashes.get(battleListCreatures[battleListIndex]['name']).copy()
            creatureNameImg3 = creatureNameImg3[:, 1:creatureNameImg3.shape[1]]
            if creatureWithDirtNameImg3.shape[1] != creatureNameImg3.shape[1]:
                creatureNameImg3 = creatureNameImg3[:, 0:creatureNameImg3.shape[1] - 1]
            if hasMatrixInsideOther(creatureWithDirtNameImg3, creatureNameImg3):
                creature = makeCreature(battleListCreatures[battleListIndex]['name'], 'monster', creaturesBars[creatureBarSortedIndex], direction, gameWindowCoordinate, gameWindowImage, coordinate, slotWidth, discoverTarget=discoverTarget, beingAttackedCreatureCategory=beingAttackedCreatureCategory, walkedPixelsInSqm=walkedPixelsInSqm)
                if creature[2]:
                    discoverTarget = False
                creatures.append(creature)
                break
            nonCreaturesForCurrentBar[battleListCreatures[battleListIndex]['name']] = True
    return np.array(creatures, dtype=Creature)


# TODO: add unit tests
# TODO: add perf
# TODO: add typings
# TODO: change to for loop with numba
def getCreaturesByType(gameWindowCreatures: CreatureList, creatureType):
    return gameWindowCreatures[gameWindowCreatures['type'] == creatureType]


# TODO: add unit tests
# TODO: add perf
# TODO: add typings
def getCreaturesGraph(gameWindowCreatures: CreatureList, coordinate: Coordinate):
    floorLevel = gameWindowCreatures[0]['coordinate'][2]
    walkableFloorsSqms = walkableFloorsSqms[floorLevel]
    gameWindowWalkableFloorsSqms = getGameWindowWalkableFloorsSqms(
        walkableFloorsSqms, coordinate)
    adjacencyMatrix = getAdjacencyMatrix(gameWindowWalkableFloorsSqms)
    graph = csr_matrix(adjacencyMatrix)
    playerGameWindowIndex = 82
    graphWeights = dijkstra(graph, directed=True, indices=playerGameWindowIndex, unweighted=False)
    graphWeights = graphWeights.reshape(11, 15)
    availableCreatures = [gameWindowCreature for gameWindowCreature in gameWindowCreatures if graphWeights[gameWindowCreature['slot'][1], gameWindowCreature['slot'][0]] != np.inf]
    return np.array(availableCreatures, dtype=Creature)


# TODO: add unit tests
# TODO: add perf
# TODO: improve performance
def getDifferentCreaturesBySlots(previousGameWindowCreatures: CreatureList, currentGameWindowCreatures: CreatureList, slots: List[Slot]) -> CreatureList:
    previousGameWindowCreaturesBySlots = np.array(
        [], dtype=Creature)
    currentGameWindowCreaturesBySlots = np.array(
        [], dtype=Creature)
    differentCreatures = np.array([], dtype=Creature)
    for previousGameWindowCreature in previousGameWindowCreatures:
        if np.isin(previousGameWindowCreature['slot'], slots).all():
            previousGameWindowCreaturesBySlots = np.append(
                previousGameWindowCreaturesBySlots, [previousGameWindowCreature])
    for currentGameWindowCreature in currentGameWindowCreatures:
        if np.isin(currentGameWindowCreature['slot'], slots).all():
            currentGameWindowCreaturesBySlots = np.append(
                currentGameWindowCreaturesBySlots, [currentGameWindowCreature])
    for previousGameWindowCreature in previousGameWindowCreaturesBySlots:
        creatureDoesNotExists = True
        for currentGameWindowCreature in currentGameWindowCreatures:
            previousGameWindowCreatureHash = hashitHex(
                previousGameWindowCreature)
            currentGameWindowCreatureHash = hashitHex(
                currentGameWindowCreature)
            if previousGameWindowCreatureHash == currentGameWindowCreatureHash:
                creatureDoesNotExists = False
                break
        if creatureDoesNotExists:
            differentCreatures = np.append(
                differentCreatures, [previousGameWindowCreature])
    return differentCreatures


# TODO: add unit tests
# TODO: add perf
def getGameWindowWalkableFloorsSqms(walkableFloorsSqms: np.ndarray, coordinate: Coordinate) -> np.ndarray:
    (xOfPixelCoordinate, yOfPixelCoordinate) = getPixelFromCoordinate(
        coordinate)
    return walkableFloorsSqms[yOfPixelCoordinate -
                                               5:yOfPixelCoordinate+6, xOfPixelCoordinate-7:xOfPixelCoordinate+8].copy()


# TODO: add unit tests
# TODO: add perf
# TODO: if something is already compared, avoid it. Check if it is faster
@njit(cache=True, fastmath=True)
def getNearestCreaturesCount(creatures: CreatureList) -> int:
    nearestCreaturesCount = 0
    for creatureSlot in creatures['slot']:
        if (creatureSlot[0] == 6 and creatureSlot[1] == 4) or (creatureSlot[0] == 7 and creatureSlot[1] == 4) or (creatureSlot[0] == 8 and creatureSlot[1] == 4) or (creatureSlot[0] == 6 and creatureSlot[1] == 5) or (creatureSlot[0] == 8 and creatureSlot[1] == 5) or (creatureSlot[0] == 6 and creatureSlot[1] == 6) or (creatureSlot[0] == 7 and creatureSlot[1] == 6) or (creatureSlot[0] == 8 and creatureSlot[1] == 6):
            nearestCreaturesCount += 1
    return nearestCreaturesCount


# TODO: add unit tests
# TODO: add perf
@njit(cache=True, fastmath=True)
def getTargetCreature(gameWindowCreatures: CreatureList):
    if len(gameWindowCreatures) == 0:
        return None
    for gameWindowCreature in gameWindowCreatures:
        if gameWindowCreature['isBeingAttacked']:
            return gameWindowCreature


# TODO: add unit tests
# TODO: add perf
def hasTargetToCreatureBySlot(gameWindowCreatures: CreatureList, slot: Slot, coordinate: Coordinate) -> bool:
    if len(gameWindowCreatures) == 0:
        return False
    xOfCoordinate, yOfCoordinate, floorLevel = coordinate
    gameWindowWalkableFloorsSqms = getGameWindowWalkableFloorsSqms(
        walkableFloorsSqms[floorLevel], coordinate)
    creaturesSlots = gameWindowCreatures['slot'][:, [1, 0]]
    gameWindowWalkableFloorsSqms[creaturesSlots[:, 0], creaturesSlots[:, 1]] = 0
    gameWindowWalkableFloorsSqms[slot[1], slot[0]] = 1
    pf = tcod.path.AStar(gameWindowWalkableFloorsSqms, 0)
    xOfGoalCoordinate = coordinate[0] + slot[0] - 7
    yOfGoalCoordinate = coordinate[1] + slot[1] - 5
    x = xOfGoalCoordinate - xOfCoordinate + 7
    y = yOfGoalCoordinate - yOfCoordinate + 5
    paths = pf.get_path(5, 7, y, x)
    walkpoints = [[xOfCoordinate + x - 7,
                   yOfCoordinate + y - 5, floorLevel] for y, x in paths]
    return len(walkpoints) > 0


# TODO: add unit tests
# TODO: add perf
def hasTargetToCreature(gameWindowCreatures: CreatureList, gameWindowCreature: Creature, coordinate: Coordinate) -> bool:
    hasTarget = hasTargetToCreatureBySlot(
        gameWindowCreatures, gameWindowCreature['slot'], coordinate)
    return hasTarget


# TODO: add unit tests
# TODO: add perf
# TODO: is possible to do at same time since everything is 64 pixels or per type(horizontal, vertical) of bar
@njit(cache=True, fastmath=True)
def isCreatureBeingAttacked(gameWindowImage: GrayImage, borderX: int, yOfCreatureBar: int, slotWidth: int) -> bool:
    pixelsCount = 0
    borderedCreatureImg = gameWindowImage[yOfCreatureBar + 5:yOfCreatureBar +
                                    5 + slotWidth, borderX:borderX + slotWidth]
    borderGap = 4 if slotWidth == 64 else 2
    yOfBorder = slotWidth - borderGap
    topBorder = borderedCreatureImg[0:borderGap, :].flatten()
    for i in range(len(topBorder)):
        if topBorder[i] == 76 or topBorder[i] == 166:
            pixelsCount += 1
            if pixelsCount > 50:
                return True
    leftBorder = borderedCreatureImg[borderGap:yOfBorder, 0:borderGap].flatten()
    for i in range(len(leftBorder)):
        if leftBorder[i] == 76 or leftBorder[i] == 166:
            pixelsCount += 1
            if pixelsCount > 50:
                return True
    rightBorder = borderedCreatureImg[borderGap:yOfBorder, yOfBorder:].flatten()
    for i in range(len(rightBorder)):
        if rightBorder[i] == 76 or rightBorder[i] == 166:
            pixelsCount += 1
            if pixelsCount > 50:
                return True
    bottomBorder = borderedCreatureImg[yOfBorder:, :].flatten()
    for i in range(len(bottomBorder)):
        if bottomBorder[i] == 76 or bottomBorder[i] == 166:
            pixelsCount += 1
    return pixelsCount > 50


# TODO: add unit tests
# TODO: add perf
# TODO: add typings
# TODO: windowCoordinate should be improved for gameWindow edges
# TODO: detect being attacked creature by category
# TODO: since there is only one creature in gameWindow and one in battleList being attacked, avoid computing if creature is being attacked on gameWindow
def makeCreature(creatureName: str, creatureType: str, creatureBar: Tuple[int, int], direction: str, gameWindowCoordinate: XYCoordinate, gameWindowImage: GrayImage, coordinate: Coordinate, slotWidth: SlotWidth, discoverTarget: bool=True, beingAttackedCreatureCategory: Union[str, None]=None, walkedPixelsInSqm: int=0):
    isBigGameWindow = slotWidth == 64
    gameWindowMisalignment = {'x': 0, 'y': 0}
    if creatureType == 'monster':
        gameWindowMisalignment = wikiCreatures.get(creatureName).get('gameWindowMisalignment', {'x': 0, 'y': 0})
    gameWindowMisalignmentX = gameWindowMisalignment['x'] if isBigGameWindow else gameWindowMisalignment['x'] / 2
    gameWindowMisalignmentY = gameWindowMisalignment['y'] if isBigGameWindow else gameWindowMisalignment['y'] / 2
    distanceBetweenSlotPixelLifeBar = 19 if isBigGameWindow else 3
    xCoordinate = creatureBar[0] - distanceBetweenSlotPixelLifeBar
    # xCoordinate = xCoordinate - walkedPixelsInSqm if direction == 'left' else xCoordinate + walkedPixelsInSqm
    xSlot = max(min(round((xCoordinate + gameWindowMisalignmentX) / slotWidth), 14), 0)
    yCoordinate = 0 if creatureBar[1] <= 14 else creatureBar[1] + 5
    ySlot = max(min(round((yCoordinate + gameWindowMisalignmentY) / slotWidth), 10), 0)
    borderX = max(creatureBar[0] - distanceBetweenSlotPixelLifeBar, 0)
    isBeingAttacked = False
    if discoverTarget and beingAttackedCreatureCategory is not None and beingAttackedCreatureCategory == creatureName:
        isBeingAttacked = isCreatureBeingAttacked(gameWindowImage, borderX, creatureBar[1], slotWidth)
    slot = (xSlot, ySlot)
    coordinate = [coordinate[0] - 7 + xSlot, coordinate[1] - 5 + ySlot, coordinate[2]]
    if not isCoordinateWalkable(coordinate):
        if direction == 'left' or direction == 'right':
            leftCoordinate = [coordinate[0] - 1, coordinate[1], coordinate[2]]
            if isCoordinateWalkable(leftCoordinate):
                coordinate = leftCoordinate
                xSlot = slot[0] - 1
                xSlot = min(xSlot, 14)
                xSlot = max(xSlot, 0)
                slot = (xSlot, slot[1])
            else:
                rightCoordinate = [coordinate[0] + 1, coordinate[1], coordinate[2]]
                if isCoordinateWalkable(rightCoordinate):
                    coordinate = rightCoordinate
                    xSlot = slot[0] + 1
                    xSlot = min(xSlot, 14)
                    xSlot = max(xSlot, 0)
                    slot = (xSlot, slot[1])
        if direction == 'top' or direction == 'bottom':
            topCoordinate = [coordinate[0], coordinate[1] - 1, coordinate[2]]
            if isCoordinateWalkable(topCoordinate):
                coordinate = topCoordinate
                ySlot = slot[1] - 1
                ySlot = min(ySlot, 10)
                ySlot = max(ySlot, 0)
                slot = (slot[0], ySlot)
            else:
                bottomCoordinate = [coordinate[0], coordinate[1] + 1, coordinate[2]]
                if isCoordinateWalkable(bottomCoordinate):
                    coordinate = bottomCoordinate
                    ySlot = slot[1] + 1
                    ySlot = min(ySlot, 10)
                    ySlot = max(ySlot, 0)
                    slot = (slot[0], ySlot)
    halfOfSlot = (slotWidth / 2)
    xCoordinate = min(max(xCoordinate + halfOfSlot, halfOfSlot), gameWindowImage.shape[1] - halfOfSlot)
    yCoordinate = min(max(yCoordinate + halfOfSlot, halfOfSlot), gameWindowImage.shape[0] - halfOfSlot)
    windowCoordinate = (gameWindowCoordinate[0] + xCoordinate, gameWindowCoordinate[1] + yCoordinate)
    gameWindowCoordinate = (xCoordinate + gameWindowMisalignmentX, yCoordinate + gameWindowMisalignmentY)
    isUnderRoof = gameWindowImage[creatureBar[1] + 1, creatureBar[0] + 1] == 192
    return (creatureName, creatureType, isBeingAttacked, slot, coordinate, windowCoordinate , gameWindowCoordinate, isUnderRoof)
