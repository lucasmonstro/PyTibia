import numpy as np
from typing import List, Union
from scipy.spatial import distance
from src.shared.typings import Coordinate, CoordinateList, XYCoordinate
from .core import getPixelFromCoordinate


# TODO: add unit tests
def getAroundPixelsCoordinates(pixelCoordinate: XYCoordinate) -> List[XYCoordinate]:
    aroundPixelsCoordinatesIndexes = np.array(
        [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
    pixelCoordinates = np.broadcast_to(
        pixelCoordinate, aroundPixelsCoordinatesIndexes.shape)
    aroundPixelsCoordinates = np.add(
        aroundPixelsCoordinatesIndexes, pixelCoordinates)
    return aroundPixelsCoordinates


# TODO: add unit tests
def getAvailableAroundPixelsCoordinates(aroundPixelsCoordinates: List[XYCoordinate], walkableFloorSqms: np.ndarray) -> List[XYCoordinate]:
    yPixelsCoordinates = aroundPixelsCoordinates[:, 1]
    xPixelsCoordinates = aroundPixelsCoordinates[:, 0]
    nonzero = np.nonzero(walkableFloorSqms[yPixelsCoordinates, xPixelsCoordinates])[0]
    return np.take(
        aroundPixelsCoordinates, nonzero, axis=0)


# TODO: add unit tests
def getAvailableAroundCoordinates(coordinate: Coordinate, walkableFloorSqms: np.ndarray) -> CoordinateList:
    pixelCoordinate = getPixelFromCoordinate(coordinate)
    aroundPixelsCoordinates = getAroundPixelsCoordinates(pixelCoordinate)
    availableAroundPixelsCoordinates = getAvailableAroundPixelsCoordinates(
        aroundPixelsCoordinates, walkableFloorSqms)
    xCoordinates = availableAroundPixelsCoordinates[:, 0] + 31744
    yCoordinates = availableAroundPixelsCoordinates[:, 1] + 30976
    floors = np.broadcast_to(
        coordinate[2], (availableAroundPixelsCoordinates.shape[0]))
    return np.column_stack(
        (xCoordinates, yCoordinates, floors))


# TODO: add unit tests
def getClosestCoordinate(coordinate: Coordinate, coordinates: CoordinateList) -> Coordinate:
    xOfCoordinate, yOfCoordinate, _ = coordinate
    coordinateWithoutFloor = [xOfCoordinate, yOfCoordinate]
    coordinatesWithoutFloor = coordinates[:, [0, 1]]
    distancesOfCoordinates = distance.cdist(
        [coordinateWithoutFloor], coordinatesWithoutFloor)[0]
    sortedDistancesOfCoordinates = np.argsort(distancesOfCoordinates)
    closestCoordinateIndex = sortedDistancesOfCoordinates[0]
    closestCoordinate = coordinates[closestCoordinateIndex]
    return closestCoordinate


# TODO: add unit tests
def getDirectionBetweenCoordinates(coordinate: Coordinate, nextCoordinate: Coordinate) -> Union[str, None]:
    (xOfCurrentCoordinate, yOfCurrentCoordinate, _) = coordinate
    (xOfNextWaypointCoordinate, yOfNextWaypointCoordinate, _) = nextCoordinate
    if xOfCurrentCoordinate < xOfNextWaypointCoordinate:
        return 'right'
    if xOfNextWaypointCoordinate < xOfCurrentCoordinate:
        return 'left'
    if yOfCurrentCoordinate < yOfNextWaypointCoordinate:
        return 'down'
    if yOfNextWaypointCoordinate < yOfCurrentCoordinate:
        return 'up'
    return None
