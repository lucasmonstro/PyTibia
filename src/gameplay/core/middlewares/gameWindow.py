import numpy as np
from src.repositories.battleList.core import getBeingAttackedCreatureCategory
from src.repositories.chat.core import hasNewLoot
from src.repositories.gameWindow.config import gameWindowSizes
from src.repositories.gameWindow.core import getCoordinate, getImageByCoordinate
from src.repositories.gameWindow.creatures import getCreatures, getCreaturesByType, getDifferentCreaturesBySlots, getTargetCreature
from src.repositories.gameWindow.typings import Creature
from ...comboSpells.core import getSpellPath
from ...typings import Context
from ..tasks.selectChatTab import SelectChatTabTask


# TODO: add unit tests
def setDirectionMiddleware(gameContext: Context) -> Context:
    if gameContext['radar']['previousCoordinate'] is None:
        gameContext['radar']['previousCoordinate'] = gameContext['radar']['coordinate']
    if gameContext['radar']['coordinate'][0] != gameContext['radar']['previousCoordinate'][0] or gameContext['radar']['coordinate'][1] != gameContext['radar']['previousCoordinate'][1] or gameContext['radar']['coordinate'][2] != gameContext['radar']['previousCoordinate'][2]:
        comingFromDirection = None
        if gameContext['radar']['coordinate'][2] != gameContext['radar']['previousCoordinate'][2]:
            comingFromDirection = None
        elif gameContext['radar']['coordinate'][0] != gameContext['radar']['previousCoordinate'][0] and gameContext['radar']['coordinate'][1] != gameContext['radar']['previousCoordinate'][1]:
            comingFromDirection = None
        elif gameContext['radar']['coordinate'][0] != gameContext['radar']['previousCoordinate'][0]:
            comingFromDirection = 'left' if gameContext['radar']['coordinate'][0] > gameContext['radar']['previousCoordinate'][0] else 'right'
        elif gameContext['radar']['coordinate'][1] != gameContext['radar']['previousCoordinate'][1]:
            comingFromDirection = 'top' if gameContext['radar']['coordinate'][1] > gameContext['radar']['previousCoordinate'][1] else 'bottom'
        gameContext['comingFromDirection'] = comingFromDirection
    # if gameContext['gameWindow']['previousGameWindowImage'] is not None:
    #     gameContext['gameWindow']['walkedPixelsInSqm'] = getWalkedPixels(gameContext)
    gameContext['gameWindow']['previousGameWindowImage'] = gameContext['gameWindow']['image']
    gameContext['radar']['previousCoordinate'] = gameContext['radar']['coordinate']
    return gameContext


# TODO: add unit tests
def setHandleLootMiddleware(gameContext: Context) -> Context:
    endlessTasks = ['depositGold', 'refill', 'selectLootTab']
    # if (gameContext['currentTask'] is None or gameContext['currentTask'].name not in endlessTasks):
    #     lootTab = gameContext['chat']['tabs'].get('loot')
    #     hasChatTab = lootTab is not None
    #     if hasChatTab and not lootTab['isSelected']:
    #         gameContext['currentTask'] = SelectChatTabTask('loot')
    if hasNewLoot(gameContext['screenshot']):
        if gameContext['cavebot']['previousTargetCreature'] is not None:
            gameContext['loot']['corpsesToLoot'] = np.append(gameContext['loot']['corpsesToLoot'], [gameContext['cavebot']['previousTargetCreature']], axis=0)
            gameContext['cavebot']['previousTargetCreature'] = None
        hasSpelledExoriCategory = gameContext['comboSpells']['lastUsedSpell'] is not None and gameContext['comboSpells']['lastUsedSpell'] in ['exori', 'exori gran', 'exori mas']
        if hasSpelledExoriCategory:
            spellPath = getSpellPath(gameContext['comboSpells']['lastUsedSpell'])
            if len(spellPath) > 0:
                differentCreatures = getDifferentCreaturesBySlots(gameContext['gameWindow']['previousMonsters'], gameContext['gameWindow']['monsters'], spellPath)
                gameContext['loot']['corpsesToLoot'] = np.append(gameContext['loot']['corpsesToLoot'], differentCreatures, axis=0)
            gameContext['comboSpells']['lastUsedSpell'] = None
    gameContext['cavebot']['targetCreature'] = getTargetCreature(gameContext['gameWindow']['monsters'])
    if gameContext['cavebot']['targetCreature'] is not None:
        gameContext['cavebot']['previousTargetCreature'] = gameContext['cavebot']['targetCreature']
    return gameContext


# TODO: add unit tests
def setGameWindowMiddleware(gameContext: Context) -> Context:
    gameWindowSize = gameWindowSizes[gameContext['resolution']]
    gameContext['gameWindow']['coordinate'] = getCoordinate(
        gameContext['screenshot'], gameWindowSize)
    gameContext['gameWindow']['image'] = getImageByCoordinate(
        gameContext['screenshot'], gameContext['gameWindow']['coordinate'], gameWindowSize)
    return gameContext


# TODO: add unit tests
def setGameWindowCreaturesMiddleware(gameContext: Context) -> Context:
    beingAttackedCreatureCategory = getBeingAttackedCreatureCategory(gameContext['battleList']['creatures'])
    gameContext['battleList']['beingAttackedCreatureCategory'] = beingAttackedCreatureCategory
    gameContext['gameWindow']['creatures'] = getCreatures(
        gameContext['battleList']['creatures'], gameContext['comingFromDirection'], gameContext['gameWindow']['coordinate'], gameContext['gameWindow']['image'], gameContext['radar']['coordinate'], beingAttackedCreatureCategory=beingAttackedCreatureCategory, walkedPixelsInSqm=gameContext['gameWindow']['walkedPixelsInSqm'])
    hasNoGameWindowCreatures = len(gameContext['gameWindow']['creatures']) == 0
    gameContext['gameWindow']['monsters'] = np.array([], dtype=Creature) if hasNoGameWindowCreatures else getCreaturesByType(gameContext['gameWindow']['creatures'], 'monster')
    gameContext['gameWindow']['players'] = np.array([], dtype=Creature) if hasNoGameWindowCreatures else getCreaturesByType(gameContext['gameWindow']['creatures'], 'player')
    return gameContext
