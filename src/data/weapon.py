import sys
from data.constants import SCORELIST, PROFICIENCYLIST

class Weapon:
    def __init__(self, name, score, level, scoreValue, dice, types, proficiency="Untrained"):
        self.__name = str(name)
        self.__score = score
        self.__scoreValue = int(scoreValue)
        self.__proficiency = proficiency
        self.__level = int(level)
        self.__item = 0
        self.__damageDice = dice
        self.__type = None
        self.__description = None

        if score not in SCORELIST:
            raise NameError("That is not a valid Score")
        if proficiency not in PROFICIENCYLIST:
            raise NameError("That is not a valid Proficiency")

    def getWeapon(self):
        return self.__name

    def getBonus(self):
        if self.__proficiency == "Untrained":
            proficiency = 0
        else:
            proficiency = PROFICIENCYLIST[self.__proficiency] + self.__level
        return int(((self.__scoreValue - 10) // 2) + proficiency + self.__item), self.__damageDice, self.__type

    def getScore(self):
        return self.__score

    def getScoreValue(self):
        return self.__scoreValue

    def setScoreValue(self, newValue):
        self.__scoreValue = int(newValue)

    def getItem(self):
        return self.__item

    def setLevel(self, newValue):
        self.__level = newValue

    def getProficiency(self):
        return self.__proficiency

    def setProficiency(self, newValue):
        if newValue not in PROFICIENCYLIST:
            raise NameError("That proficiency in not valid: " + str(newValue))
        self.__proficiency = newValue

    def setDice(self, dice):
        self.__damageDice = dice

    def getDice(self):
        return self.__damageDice

    def setType(self, type):
        self.__type = type

    def getType(self):
        return self.__type

    def getDescription(self):
        return self.__description

    def setDescription(self, newValue):
        self.__description = newValue