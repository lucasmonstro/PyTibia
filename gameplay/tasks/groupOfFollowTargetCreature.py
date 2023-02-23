import numpy as np
from scipy.spatial import distance
from time import time
from radar.types import coordinateType
from ..factories.makeWalkTask import makeWalkTask
from ..typings import taskType
from ..waypoint import generateFloorWalkpoints
from .base.vector import VectorTask


class GroupOfFollowTargetCreatureTasks(VectorTask):
    def __init__(self, context):
        super().__init__()
        self.createdAt = time()
        self.startedAt = None
        self.finishedAt = None
        self.delayBeforeStart = 0
        self.delayAfterComplete = 0
        self.name = 'groupOfFollowTargetCreature'
        self.tasks = self.generateTasks(context)

    def generateTasks(self, context):
        tasks = np.array([], dtype=taskType)
        nonWalkableCoordinates = context['cavebot']['holesOrStairs'].copy()
        for monster in context['monsters']:
            if np.array_equal(monster['coordinate'], context['cavebot']['targetCreature']['coordinate']) == False:
                monsterCoordinateTuple = (monster['coordinate'][0], monster['coordinate'][1], monster['coordinate'][2])
                coordinatesToAppend = np.array([monsterCoordinateTuple], dtype=coordinateType)
                nonWalkableCoordinates = np.append(nonWalkableCoordinates, coordinatesToAppend)
        hudHeight, hudWidth  = context['hudImg'].shape
        hudCenter = (hudWidth // 2, hudHeight // 2)
        monsterHudCoordinate = context['cavebot']['targetCreature']['hudCoordinate']
        moduleX = abs(hudCenter[0] - monsterHudCoordinate[0])
        moduleY = abs(hudCenter[1] - monsterHudCoordinate[1])
        dist = distance.cdist([context['coordinate']], [context['cavebot']['targetCreature']['coordinate']]).flatten()[0]
        walkpoints = []
        if dist < 2:
            if moduleX > 64 or moduleY > 64:
                walkpoints.append(context['cavebot']['targetCreature']['coordinate'])
        else:
            walkpoints = generateFloorWalkpoints(
                context['coordinate'], context['cavebot']['targetCreature']['coordinate'], nonWalkableCoordinates=nonWalkableCoordinates)
            hasWalkpoints = len(walkpoints) > 0
            if hasWalkpoints:
                walkpoints.pop()
        for walkpoint in walkpoints:
            walkpointTask = makeWalkTask(context, walkpoint)
            taskToAppend = np.array([walkpointTask], dtype=taskType)
            tasks = np.append(tasks, [taskToAppend])
        return tasks

    def shouldIgnore(self, _):
        return False

    def shouldRestart(self, _):
        return False

    def onIgnored(self, context):
        return context

    def onDidComplete(self, context):
        return context
