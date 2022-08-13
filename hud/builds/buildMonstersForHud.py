import utils.core, utils.image
from wiki import creatures
import numpy as np

messLetters = ['t', 'T', 'r', 'R', 'f', 'F', 'L']

for monster in creatures.creatures:
    monsterLetters = np.zeros((11, 0), dtype=np.uint8)
    for index, letter in enumerate(monster):
        letter = letter if letter != ' ' else 'space'
        letter = letter if letter != '.' else 'dot'
        letterBasePath = 'hud/images/letters/uppercase' if letter.isupper() else 'hud/images/letters/lowercase'
        letterFullPath = '{0}/{1}.png'.format(letterBasePath, letter)
        letterAsArray = utils.image.loadAsArray(letterFullPath).copy()
        letterAsArray[np.nonzero(letterAsArray == 0)] = 1
        letterAsArray[np.nonzero(letterAsArray == 255)] = 0
        if index > 0:
            previousLetter = monster[index - 1]
            previousLetterIsMessLetter = (previousLetter == 't' or previousLetter == 'T' or previousLetter == 'r' or previousLetter == 'R' or previousLetter == 'f' or previousLetter == 'L')
            letterIsMessLetter = (letter == 't' or letter == 'T' or letter == 'f' or letter == 'J')
            if previousLetterIsMessLetter or letterIsMessLetter:
                size = 2 if previousLetterIsMessLetter and letterIsMessLetter else 1
                ultimaFileiraDaImagem = monsterLetters[:, monsterLetters.shape[1] - size:monsterLetters.shape[1]]
                primeiraFileiraDaProximaLetra = letterAsArray[:, 0:size]
                somaDasDuas = np.add(ultimaFileiraDaImagem, primeiraFileiraDaProximaLetra)
                monsterLetters = monsterLetters[:, 0:monsterLetters.shape[1] - size]
                monsterLetters = np.hstack((monsterLetters, somaDasDuas))
                restoDaProximaLetra = letterAsArray[:, size:letterAsArray.shape[1]]
                monsterLetters = np.hstack((monsterLetters, restoDaProximaLetra))
            else:
                monsterLetters = np.hstack((monsterLetters, letterAsArray)) 
        else:
            monsterLetters = np.hstack((monsterLetters, letterAsArray))
    monsterLetters[np.nonzero(monsterLetters == 0)] = 255
    monsterLetters[np.nonzero(monsterLetters == 1)] = 0
    monsterLetters[np.nonzero(monsterLetters == 2)] = 0
    utils.image.saveFromArray(monsterLetters, 'hud/images/monsters/{}.png'.format(monster))