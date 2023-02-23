import dxcam
import multiprocessing
import numpy as np
import pyautogui
from rx import interval, operators
from rx.scheduler import ThreadPoolScheduler
from time import sleep, time
import actionBar.core
import battleList.core
import battleList.typing
import chat.core
import gameplay.cavebot
import gameplay.decision
from gameplay.tasks.groupOfLootCorpse import GroupOfLootCorpseTasks
import gameplay.resolvers
import gameplay.typings
import gameplay.waypoint
import hud.core
import hud.creatures
import hud.slot
import player.core
import radar.core
from radar.types import coordinateType, waypointType
import utils.array
import utils.core
import utils.image
import skills.core


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


camera = dxcam.create()
gameContext = {
    'backpacks': {
        'main': 'brocade backpack',
        'gold': 'beach backpack',
        'loot': 'fur backpack',
    },
    'battleListCreatures': np.array([], dtype=battleList.typing.creatureType),
    'cavebot': {
        'holesOrStairs': np.array([
            (33306, 32284, 5),
            (33306, 32284, 6),
            (33309, 32284, 6),
            (33312, 32281, 7),
            (33309, 32284, 7),
            (33312, 32281, 8),
            (33300, 32290, 8),
        ], dtype=coordinateType),
        'isAttackingSomeCreature': False,
        'running': True,
        'targetCreature': None,
        'waypoints': {
            'currentIndex': None,
            'points': np.array([
                ('', 'depositItems', (33214, 32456, 8), {'city': 'darashia'}),
                ('', 'walk', (33214, 32459, 8), {}),
                ('', 'walk', (33214, 32456, 8), {}),
                ('', 'moveUpNorth', (33214, 32456, 8), {}),
                ('', 'walk', (33214, 32450, 7), {}),  #indo para cave
                ('', 'walk', (33220, 32428, 7), {}),
                ('', 'walk', (33216, 32392, 7), {}),
                ('', 'walk', (33251, 32364, 7), {}),
                ('', 'walk', (33277, 32329, 7), {}),
                ('', 'walk', (33301, 32291, 7), {}),
                ('', 'walk', (33302, 32289, 7), {}), # chegou na cave
                ('caveStart', 'walk', (33301, 32278, 7), {}), # 10
                ('', 'walk', (33312, 32278, 7), {}), # 11
                ('', 'walk', (33318, 32283, 7), {}), # 12
                ('', 'walk', (33312, 32280, 7), {}), # 13
                ('', 'moveDownSouth', (33312, 32280, 7), {}), # 14
                ('', 'walk', (33302, 32283, 8), {}), # 15
                ('', 'walk', (33300, 32289, 8), {}), # 16
                ('', 'moveDownSouth', (33300, 32289, 8), {}), # 17
                ('', 'walk', (33302, 32281, 9), {}), # 18
                ('', 'walk', (33312, 32280, 9), {}), # 19
                ('', 'walk', (33312, 32289, 9), {}), # 20
                ('', 'walk', (33300, 32291, 9), {}), # 21
                ('', 'moveUpNorth', (33300, 32291, 9), {}), # 22
                ('', 'walk', (33302, 32283, 8), {}), # 23
                ('', 'walk', (33312, 32282, 8), {}), # 24
                ('', 'moveUpNorth', (33312, 32282, 8), {}), # 25
                ('', 'walk', (33311, 32285, 7), {}), # 26
                ('', 'walk', (33309, 32285, 7), {}), # 27
                ('', 'moveUpNorth', (33309, 32285, 7), {}), # 28
                ('', 'walk', (33310, 32278, 6), {}), # 29
                ('', 'walk', (33309, 32283, 6), {}), # 30
                ('', 'moveDownSouth', (33309, 32283, 6), {}), # 31
                ('', 'walk', (33305, 32289, 7), {}), # 32
                ('', 'refillChecker', (33306, 32289, 7), { # 33
                    'minimumOfManaPotions': 1,
                    'minimumOfHealthPotions': 1,
                    'minimumOfCapacity': 200,
                    'waypointLabelToRedirect': 'caveStart',
                }),
                ('', 'walk', (33264,32321,7), {}), # 31
            ], dtype=waypointType),
            'state': None
        },
    },
    'comingFromDirection': None,
    'corpsesToLoot': np.array([], dtype=hud.creatures.creatureType),
    'currentTask': None,
    'healing': {
        'minimumToBeHealedUsingPotion': 60,
        'minimumToBeHealedUsingSpell': 85,
        'cureSpell': 'exura med ico',
    },
    'hotkeys': {
        'eatFood': 'f7',
        'healthPotion': 'f1',
        'manaPotion': 'f2',
        'cure': 'f3',
        'rope': 'f8',
        'shovel': 'f9',
    },
    'hud': {
        'coordinate': None,
        'img': None,
    },
    'lastCoordinateVisited': None,
    'lastPressedKey': None,
    'lastWay': 'waypoint',
    'monsters': np.array([], dtype=hud.creatures.creatureType),
    'players': np.array([], dtype=hud.creatures.creatureType),
    'previousCoordinate': None,
    'coordinate': None,
    'refill': {
        'health': {
            'item': 'health potion',
            'quantity': 140,
        },
        'mana': {
            'item': 'mana potion',
            'quantity': 30,
        },
    },
    'resolution': 1080,
    'targetCreature': None,
    'screenshot': None,
    'way': None,
    'window': None
}
hudCreatures = np.array([], dtype=hud.creatures.creatureType)


def main():
    optimal_thread_count = multiprocessing.cpu_count()
    threadPoolScheduler = ThreadPoolScheduler(optimal_thread_count)
    thirteenFps = 0.00416666666
    fpsObserver = interval(thirteenFps)

    def handleScreenshot(_):
        global gameContext
        rgbScreenshot = utils.core.getScreenshot(camera)
        grayScreenshot = utils.image.RGBtoGray(rgbScreenshot)
        gameContext['screenshot'] = grayScreenshot
        return gameContext

    fpsWithScreenshot = fpsObserver.pipe(
        operators.map(handleScreenshot),
    )

    def handleCoordinate(context):
        global gameContext
        context['coordinate'] = radar.core.getCoordinate(
            context['screenshot'], previousCoordinate=context['previousCoordinate'])
        context['previousCoordinate'] = context['coordinate']
        gameContext = context
        return context

    coordinatesObserver = fpsWithScreenshot.pipe(
        operators.filter(lambda result: result['screenshot'] is not None),
        operators.filter(
            lambda _: gameContext['cavebot']['running'] == True),
        operators.map(handleCoordinate)
    )

    def handleBattleListCreatures(context):
        global gameContext
        copyOfContext = context.copy()
        copyOfContext['battleListCreatures'] = battleList.core.getCreatures(
            copyOfContext['screenshot'])
        hasBattleListCreatures = len(copyOfContext['battleListCreatures']) > 0
        copyOfContext['cavebot']['isAttackingSomeCreature'] = battleList.core.isAttackingSomeCreature(context['battleListCreatures']) if hasBattleListCreatures else False
        gameContext = copyOfContext
        return copyOfContext

    battleListObserver = coordinatesObserver.pipe(
        operators.map(handleBattleListCreatures)
    )

    def handleHudCoordinate(context):
        global gameContext
        copyOfContext = context.copy()
        hudSize = hud.core.hudSizes[copyOfContext['resolution']]
        copyOfContext['hud']['coordinate'] = hud.core.getCoordinate(
            copyOfContext['screenshot'], hudSize)
        gameContext = copyOfContext
        return copyOfContext

    hudCoordinateObserver = battleListObserver.pipe(
        operators.filter(lambda result: result['coordinate'] is not None),
        operators.map(handleHudCoordinate)
    )

    def handleHudImg(context):
        global gameContext
        copyOfContext = context.copy()
        hudSize = hud.core.hudSizes[copyOfContext['resolution']]
        copyOfContext['hudImg'] = hud.core.getImgByCoordinate(
            copyOfContext['screenshot'], copyOfContext['hud']['coordinate'], hudSize)
        gameContext = copyOfContext
        return copyOfContext

    hudImgObserver = hudCoordinateObserver.pipe(
        operators.map(handleHudImg)
    )

    def resolveDirection(context):
        global gameContext
        copyOfContext = context.copy()
        comingFromDirection = None
        if copyOfContext['previousCoordinate'] is None:
            copyOfContext['previousCoordinate'] = copyOfContext['coordinate']
        coordinateDidChange = np.all(
            copyOfContext['previousCoordinate'] == copyOfContext['coordinate']) == False
        if coordinateDidChange:
            coordinate = copyOfContext['coordinate']
            if coordinate[2] != copyOfContext['previousCoordinate'][2]:
                comingFromDirection = None
            elif coordinate[0] != copyOfContext['previousCoordinate'][0] and coordinate[1] != copyOfContext['previousCoordinate'][1]:
                comingFromDirection = None
            elif coordinate[0] != copyOfContext['previousCoordinate'][0]:
                comingFromDirection = 'left' if coordinate[
                    0] > copyOfContext['previousCoordinate'][0] else 'right'
            elif coordinate[1] != copyOfContext['previousCoordinate'][1]:
                comingFromDirection = 'top' if coordinate[
                    1] > copyOfContext['previousCoordinate'][1] else 'bottom'
            copyOfContext['previousCoordinate'] = copyOfContext['coordinate']
        copyOfContext['comingFromDirection'] = comingFromDirection
        gameContext = copyOfContext
        return copyOfContext

    directionObserver = hudImgObserver.pipe(operators.map(resolveDirection))

    def resolveCreatures(context):
        global gameContext, hudCreatures
        copyOfContext = context.copy()
        hudCreatures = hud.creatures.getCreatures(
            copyOfContext['battleListCreatures'], copyOfContext['comingFromDirection'], copyOfContext['hud']['coordinate'], copyOfContext['hudImg'], copyOfContext['coordinate'], copyOfContext['resolution'])
        copyOfContext['monsters'] = hud.creatures.getCreaturesByType(hudCreatures, 'monster')
        copyOfContext['players'] = hud.creatures.getCreaturesByType(hudCreatures, 'player')
        copyOfContext['cavebot']['targetCreature'] = hud.creatures.getTargetCreature(copyOfContext['monsters'])
        gameContext = copyOfContext
        return copyOfContext

    hudCreaturesObserver = directionObserver.pipe(operators.map(resolveCreatures))

    def handleLoot(context):
        if context['cavebot']['targetCreature'] is not None and chat.core.hasNewLoot(context['screenshot']):
            context['corpsesToLoot'] = np.append(context['corpsesToLoot'], [context['cavebot']['targetCreature']], axis=0)
        return context

    lootObserver = hudCreaturesObserver.pipe(operators.map(handleLoot))

    def mapDecision(context):
        global gameContext
        copyOfContext = context.copy()
        copyOfContext['way'] = gameplay.decision.getWay(
            copyOfContext['corpsesToLoot'], copyOfContext['monsters'], copyOfContext['coordinate'])
        gameContext = copyOfContext
        return copyOfContext

    def mapCurrentWaypointIndex(context):
        if context['cavebot']['waypoints']['currentIndex'] == None:
            context['cavebot']['waypoints']['currentIndex'] = radar.core.getClosestWaypointIndexFromCoordinate(
                context['coordinate'], context['cavebot']['waypoints']['points'])
        return context

    decisionObserver = lootObserver.pipe(
        operators.map(mapDecision),
        operators.map(mapCurrentWaypointIndex),
    )
    
    def shouldAskForCavebotTasks(context):
        isNotCavebotWay = context['way'] != 'cavebot'
        if isNotCavebotWay:
            return False
        if context['currentTask'] is None:
            return True
        endlessTasks = ['groupOfLootCorpse', 'groupOfRefillChecker', 'groupOfSingleWalk', 'groupOfUseRope', 'groupOfUseShovel']
        should = (context['currentTask'].name not in endlessTasks)
        return should
    
    def handleTasks(context):
        global gameContext
        copyOfContext = context.copy()
        hasCurrentTask = copyOfContext['currentTask'] is not None
        # len(copyOfContext['currentTask'].tasks) == 0
        if hasCurrentTask and (copyOfContext['currentTask'].status == 'completed'):
            copyOfContext['currentTask'] = None
        if shouldAskForCavebotTasks(context):
            hasCurrentTaskAfterCheck = copyOfContext['currentTask'] is not None
            isTryingToAttackClosestCreature = hasCurrentTaskAfterCheck and (copyOfContext['currentTask'].name == 'groupOfAttackClosestCreature' or copyOfContext['currentTask'].name == 'groupOfFollowTargetCreature')
            isNotTryingToAttackClosestCreature = not isTryingToAttackClosestCreature
            if isNotTryingToAttackClosestCreature:
                newCurrentTask = gameplay.cavebot.resolveCavebotTasks(copyOfContext)
                hasCurrentTask2 = copyOfContext['currentTask'] is not None
                if hasCurrentTask2:
                    hasTargetCreature = context['cavebot']['targetCreature'] is not None or context['cavebot']['closestCreature'] is not None
                    if hasTargetCreature:
                        hasKeyPressed = copyOfContext['lastPressedKey'] is not None
                        if hasKeyPressed:
                            pyautogui.keyUp(copyOfContext['lastPressedKey'])
                            copyOfContext['lastPressedKey'] = None
                        copyOfContext['currentTask'] = newCurrentTask
                else:
                    hasNewCurrentTask = newCurrentTask is not None
                    if hasNewCurrentTask:
                        hasKeyPressed = copyOfContext['lastPressedKey'] is not None
                        if hasKeyPressed:
                            pyautogui.keyUp(copyOfContext['lastPressedKey'])
                            copyOfContext['lastPressedKey'] = None
                        copyOfContext['currentTask'] = newCurrentTask
        elif copyOfContext['way'] == 'lootCorpses':
            if copyOfContext['currentTask'] is None:
                # TODO: get closest dead corpse
                firstDeadCorpse = copyOfContext['corpsesToLoot'][0]
                copyOfContext['currentTask'] = GroupOfLootCorpseTasks(copyOfContext, firstDeadCorpse)
        elif copyOfContext['way'] == 'waypoint':
            if copyOfContext['currentTask'] == None:
                currentWaypointIndex = copyOfContext['cavebot']['waypoints']['currentIndex']
                currentWaypoint = copyOfContext['cavebot']['waypoints']['points'][currentWaypointIndex]
                copyOfContext['currentTask'] = gameplay.resolvers.resolveTasksByWaypointType(copyOfContext, currentWaypoint)
        gameContext = copyOfContext
        return copyOfContext

    def hasTaskToExecute(context):
        has = context['currentTask'] is not None
        return has

    taskObserver = decisionObserver.pipe(
        operators.map(handleTasks),
        operators.filter(hasTaskToExecute),
        operators.subscribe_on(threadPoolScheduler),
    )

    def taskObservable(context):
        global gameContext
        copyOfContext = context.copy()
        copyOfContext = context['currentTask'].exec(copyOfContext)
        copyOfContext['lastCoordinateVisited'] = context['coordinate']
        gameContext = copyOfContext
        
    healingObserver = fpsWithScreenshot.pipe(
        operators.subscribe_on(threadPoolScheduler)
    )

    def healingObservable(context):
        cures = {
            'exura infir ico': 10,
            'exura ico': 40,
            'exura med ico': 90,
            'exura gran ico': 200,
            'utura': 40,
            'utura gran': 165,
        }
        hp = player.core.getHealthPercentage(context['screenshot'])
        couldntGetHp = hp is None
        if couldntGetHp:
            return
        mana = player.core.getManaPercentage(context['screenshot'])
        couldntGetMana = mana is None
        if couldntGetMana:
            return
        shouldHealUsingPotion = context['healing']['minimumToBeHealedUsingPotion'] >= hp
        if shouldHealUsingPotion:
            pyautogui.press(context['hotkeys']['healthPotion'])
            sleep(0.25)
            return
        shouldHealUsingSpell = context['healing']['minimumToBeHealedUsingSpell'] >= hp
        if shouldHealUsingSpell:
            hasEnoughMana = mana >= cures[context['healing']['cureSpell']]
            if hasEnoughMana:
                pyautogui.press(context['hotkeys']['cure'])
                sleep(0.25)

    spellObserver = fpsWithScreenshot.pipe(
        operators.subscribe_on(threadPoolScheduler)
    )
    
    def spellObservable(context):
        global hudCreatures
        mana = skills.core.getMana(context['screenshot'])
        couldntGetMana = mana is None
        if couldntGetMana:
            return
        canHaste = not player.core.hasSpecialCondition(context['screenshot'], 'haste')
        if mana > 60 and canHaste:
            pyautogui.press('f6')
            return
        if mana >= 115 and hud.creatures.getNearestCreaturesCount(hudCreatures) > 2 and not actionBar.core.hasExoriCooldown(context['screenshot']):
            pyautogui.press('f4')

    try:
        spellObserver.subscribe(spellObservable)
        healingObserver.subscribe(healingObservable)
        taskObserver.subscribe(taskObservable)
        while True:
            sleep(1)
            continue
    except KeyboardInterrupt:
        raise SystemExit


if __name__ == '__main__':
    main()
