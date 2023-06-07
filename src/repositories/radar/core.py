import numpy as np
from scipy.spatial import distance
from typing import Union
from src.shared.typings import Coordinate, GrayImage, GrayPixel, Waypoint, WaypointList
from src.utils.core import getCoordinateFromPixel, getPixelFromCoordinate, hashit, hashitHex, locate
from .config import coordinates, dimensions, floorsImgs, floorsLevelsImgsHashes, floorsPathsSqms, nonWalkablePixelsColors, walkableFloorsSqms
from .extractors import getRadarImage
from .locators import getRadarToolsPosition
from .typings import FloorLevel, TileFriction


# TODO: add unit tests
# TODO: add perf
# TODO: get by cached images coordinates hashes
def getCoordinate(screenshot: GrayImage, previousCoordinate: Coordinate=None) -> Union[Coordinate, None]:
    floorLevel = getFloorLevel(screenshot)
    if floorLevel is None:
        return None
    radarToolsPosition = getRadarToolsPosition(screenshot)
    if radarToolsPosition is None:
        return None
    radarImage = getRadarImage(screenshot, radarToolsPosition)
    radarHashedImg = hashitHex(radarImage)
    # TODO: use get instead
    if radarHashedImg in coordinates:
        return coordinates[radarHashedImg]
    if previousCoordinate is not None:
        (previousCoordinateXPixel, previousCoordinateYPixel) = getPixelFromCoordinate(
            previousCoordinate)
        paddingSize = 20
        yStart = previousCoordinateYPixel - \
            (dimensions['halfHeight'] + paddingSize)
        yEnd = previousCoordinateYPixel + \
            (dimensions['halfHeight'] + 1 + paddingSize)
        xStart = previousCoordinateXPixel - \
            (dimensions['halfWidth'] + paddingSize)
        xEnd = previousCoordinateXPixel + \
            (dimensions['halfWidth'] + paddingSize)
        areaImgToCompare = floorsImgs[floorLevel][yStart:yEnd, xStart:xEnd]
        areaFoundImg = locate(
            areaImgToCompare, radarImage, confidence=0.9)
        if areaFoundImg:
            currentCoordinateXPixel = previousCoordinateXPixel - \
                paddingSize + areaFoundImg[0]
            currentCoordinateYPixel = previousCoordinateYPixel - \
                paddingSize + areaFoundImg[1]
            (currentCoordinateX, currentCoordinateY) = getCoordinateFromPixel(
                (currentCoordinateXPixel, currentCoordinateYPixel))
            return [currentCoordinateX, currentCoordinateY, floorLevel]
    imgCoordinate = locate(floorsImgs[floorLevel], radarImage, confidence=0.75)
    if imgCoordinate is None:
        return None
    xImgCoordinate = imgCoordinate[0] + dimensions['halfWidth']
    yImgCoordinate = imgCoordinate[1] + dimensions['halfHeight']
    xCoordinate, yCoordinate = getCoordinateFromPixel(
        (xImgCoordinate, yImgCoordinate))
    return [xCoordinate, yCoordinate, floorLevel]


# TODO: add unit tests
# TODO: add perf
def getFloorLevel(screenshot: GrayImage) -> Union[FloorLevel, None]:
    radarToolsPosition = getRadarToolsPosition(screenshot)
    if radarToolsPosition is None:
        return None
    left, top, width, height = radarToolsPosition
    left = left + width + 8
    top = top - 7
    height = 67
    width = 2
    floorLevelImg = screenshot[top:top + height, left:left + width]
    floorImgHash = hashit(floorLevelImg)
    if floorImgHash not in floorsLevelsImgsHashes:
        return None
    return floorsLevelsImgsHashes[floorImgHash]


# TODO: add unit tests
# TODO: add perf
def getClosestWaypointIndexFromCoordinate(coordinate: Coordinate, waypoints: WaypointList) -> Waypoint:
    (xOfCoordinate, yOfCoordinate, floorLevel) = coordinate
    currentCoordinateWithoutFloor = [xOfCoordinate, yOfCoordinate]
    waypointsCoordinatesWithoutFloor = waypoints['coordinate'][:, :-1]
    waypointsCoordinatesDistances = distance.cdist(
        waypointsCoordinatesWithoutFloor, [currentCoordinateWithoutFloor]).flatten()
    waypointsIndexesOfCurrentFloor = np.nonzero(
        waypoints['coordinate'][:, 2] == floorLevel)[0]
    waypointsCoordinatesDistancesOfCurrentFloor = waypointsCoordinatesDistances[
        waypointsIndexesOfCurrentFloor]
    lowestWaypointIndex = np.argmin(
        waypointsCoordinatesDistancesOfCurrentFloor)
    lowestWaypointIndexOfCurrentFloor = waypointsIndexesOfCurrentFloor[lowestWaypointIndex]
    return lowestWaypointIndexOfCurrentFloor


availableTilesFrictions = np.array([70, 90, 95, 100, 110, 125, 140, 150, 160, 200, 250])

breakpointTileMovementSpeed = {
    1: 850,
    2: 800,
    3: 750,
    4: 700,
    5: 650,
    6: 600,
    7: 550,
    8: 500,
    9: 450,
    10: 400,
    11: 350,
    12: 300,
    13: 250,
    14: 200,
    15: 150,
    16: 100,
    17: 50,
}

tilesFrictionsWithBreakpoints = {
    70:  np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 111, 142, 200, 342, 1070]),
    90:  np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 147, 192, 278, 499, 1842]),
    95:  np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 157, 205, 299, 543, 2096]),
    100: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 113, 135, 167, 219, 321, 592, 2382]),
    110: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 126, 150, 187, 248, 367, 696, 3060]),
    125: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 175, 219, 293, 444, 876, 4419]),
    140: np.array([0, 0, 0, 0, 0, 0, 0, 111, 125, 143, 167, 201, 254, 344, 531, 1092, 6341]),
    150: np.array([0, 0, 0, 0, 0, 0, 0, 120, 135, 155, 181, 219, 278, 380, 595, 1258, 8036]),
    160: np.array([0, 0, 0, 0, 0, 0, 116, 129, 145, 167, 196, 238, 304, 419, 663, 1443, 10167]),
    200: np.array([0, 0, 0, 114, 124, 135, 149, 167, 190, 219, 261, 322, 419, 597, 998, 2444, 25761]),
    250: np.array([117, 126, 135, 146, 160, 175, 195, 220, 252, 295, 356, 446, 598, 884, 1591, 4557, 81351]),
}


# TODO: add perf
def getBreakpointTileMovementSpeed(charSpeed: int, tileFriction: TileFriction) -> int:
    tileFrictionNotFound = tileFriction not in tilesFrictionsWithBreakpoints
    if tileFrictionNotFound:
        closestTilesFrictions = np.flatnonzero(availableTilesFrictions > tileFriction)
        hasClosestTilesFrictions = len(closestTilesFrictions) > 0
        tileFriction = availableTilesFrictions[closestTilesFrictions[0]] if hasClosestTilesFrictions else 250
    breakpoints = tilesFrictionsWithBreakpoints[tileFriction]
    availableBreakpointsIndexes = np.flatnonzero(charSpeed >= breakpoints)
    hasNoAvailableBreakpointsIndexes = len(availableBreakpointsIndexes) == 0
    if hasNoAvailableBreakpointsIndexes:
        return breakpointTileMovementSpeed[1]
    firstBreakpointIndex = availableBreakpointsIndexes[-1] + 1
    tileMovementSpeed = breakpointTileMovementSpeed.get(firstBreakpointIndex)
    return tileMovementSpeed


# TODO: add unit tests
# TODO: add perf
def getTileFrictionByCoordinate(coordinate: Coordinate) -> TileFriction:
    xOfPixelCoordinate, yOfPixelCoordinate = getPixelFromCoordinate(
        coordinate)
    floorLevel = coordinate[2]
    tileFriction = floorsPathsSqms[floorLevel,
                                          yOfPixelCoordinate, xOfPixelCoordinate]
    return tileFriction


# TODO: add unit tests
# TODO: add perf
def isCloseToCoordinate(currentCoordinate: Coordinate, possibleCloseCoordinate: Coordinate, distanceTolerance: int=10) -> bool:
    (xOfCurrentCoordinate, yOfCurrentCoordinate, _) = currentCoordinate
    XYOfCurrentCoordinate = (xOfCurrentCoordinate, yOfCurrentCoordinate)
    (xOfPossibleCloseCoordinate, yOfPossibleCloseCoordinate, _) = possibleCloseCoordinate
    XYOfPossibleCloseCoordinate = (
        xOfPossibleCloseCoordinate, yOfPossibleCloseCoordinate)
    euclideanDistance = distance.cdist(
        [XYOfCurrentCoordinate], [XYOfPossibleCloseCoordinate])
    isClose = euclideanDistance <= distanceTolerance
    return isClose


# TODO: add unit tests
# TODO: add perf
# TODO: 2 coordinates was tested. Is very hard too test all coordinates(16 floors * 2560 mapWidth * 2048 mapHeight = 83.886.080 pixels)
def isCoordinateWalkable(coordinate: Coordinate) -> bool:
    (xOfPixel, yOfPixel) = getPixelFromCoordinate(coordinate)
    return (walkableFloorsSqms[coordinate[2], yOfPixel, xOfPixel]) == 1


# TODO: add unit tests
# TODO: add perf
def isNonWalkablePixelColor(pixelColor: GrayPixel) -> bool:
    isNonWalkable = np.isin(pixelColor, nonWalkablePixelsColors)
    return isNonWalkable
