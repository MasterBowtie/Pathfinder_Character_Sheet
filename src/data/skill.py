import sys
from constants.constants import SCORELIST, PROFICIENCYLIST

class Skill:
    def __init__(self, name, score, level, scoreValue, armor=False, proficiency="Untrained"):
        self.__name = str(name)
        self.__score = score
        self.__scoreValue = int(scoreValue)  # default
        self.__proficiency = proficiency
        self.__level = int(level)
        self.__item = 0  # item bonuses
        self.__armor = armor
        self.__armorBonus = 0
        self.__armorEq = armor
        self.__description = None

        if score not in SCORELIST:
            raise NameError("That is not a valid Score")
        if proficiency not in PROFICIENCYLIST:
            raise NameError("That is not a valid Proficiency")


    def getSkill(self):
        return self.__name

    def setSkill(self, newName):
        self.__name = str(newName)

    def getBonus(self):
        if self.__proficiency == "Untrained":
            proficiency = 0
        else:
            proficiency = PROFICIENCYLIST[self.__proficiency] + self.__level
        if self.__armor is False or self.__armorEq is False:
            return int(((self.__scoreValue - 10) // 2) + proficiency + self.__item)
        else:
            return int(((self.__scoreValue - 10) // 2) + proficiency + self.__item + self.__armorBonus)

    def getScore(self):
        return self.__score

    def getScoreValue(self):
        return self.__scoreValue

    def setScoreValue(self, newValue):
        self.__scoreValue = int(newValue)

    def getItem(self):
        return self.__item

    def getArmor(self):
        return self.__armor

    def getArmorBonus(self):
        return self.__armorBonus

    def setArmorBonus(self, newValue):
        self.__armorBonus = int(newValue)

    def getArmorEq(self):
        return self.__armorEq

    def equipArmor(self):
        self.__armorEq = not self.__armorEq

    def setLevel(self, newValue):
        self.__level = newValue

    def getProficiency(self):
        return self.__proficiency

    def setProficiency(self, newValue):
        if newValue not in PROFICIENCYLIST:
            raise NameError("That proficiency in not valid: " + str(newValue))
        self.__proficiency = newValue

    def getDescription(self):
        return self.__description

    def setDescription(self, newValue):
        self.__description = newValue
