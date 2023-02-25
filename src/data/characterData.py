'''
SHIELD = ['Bonus', 'Hardness', 'MaxHP', 'Broken', 'Current']



MOVEMENT = ['Land', 'Swim', 'Climb', 'Burrow']

STRIKES = [['Melee',[]],
           ['Range',[]],
           ['Magic',[]]]

ATTACKINFO = ['Name', ['Hit', 'Bonus', 'Str', 'Proficiency', 'Item'], ['Dmg', 'dice', 'Str', 'type', 'Special', 'traits']]

FEATS = [['Ancestry', []],
         ['Skill', []],
         ['Class', []],
         ['General', []],
         ['Bonus', []]]

FEATINFO = ['Name', 'Target', 'Value', 'Description', 'Reference']

EQUIPMENT = [['Money', 'Copper', 'Silver', 'Gold', 'Platinum'],
             ['Weapons',[]],
             ['Armor', []],
             ['Consumables',[]],
             ['Other', []],
             'Bulk', 'MaxBulk']

EQUIPMENTINFO = ['Name', 'Type', 'Description', 'Amount', 'Bulk', 'Reference']

SPELLS = ['Tradition',
          ['Spell Attack', 'Bonus', 'AblMod', 'Proficiency'],
          ['Spell DC', 'Bonus', 'AblMod', 'Proficiency'],
          ['Cantrip', 'Level', []],
          ['Level 1', 'Per Day', []],
          ['Level 2', 'Per Day', []],
          ['Level 3', 'Per Day', []],
          ['Level 4', 'Per Day', []],
          ['Level 5', 'Per Day', []],
          ['Level 6', 'Per Day', []],
          ['Level 7', 'Per Day', []],
          ['Level 8', 'Per Day', []],
          ['Level 9', 'Per Day', []],
          ['Level 10', 'Per Day', []],
          ['Focus', 'Per Day', []],
          ['Ritual', 'Per Day', []]]

SPELLINFO = ['Name', 'Level', 'Traits', 'Tradition', ['Cast', 'Actions', 'Components'], ['Target', 'Range'], 'Save', 'Duration', 'Effects', 'Heightened',
             'Prepared', 'Used', 'Reference']

HITPOINTS = ['Class', 'Ancestry', 'Max', 'Current', 'Temporary']
'''
from data.skill import Skill
from reference.constants import SKILLSLIST, SAVES, PROFICIENCYLIST, ANCESTORS, SCORELIST
from reference.classConstants import CLASSES
from data.ancestry import Ancestry


class CharacterData:
    def __init__(self):
        self.__Scores = {"Str": 10, "Dex": 10, "Con": 10, "Int": 10, "Wis": 10, "Cha": 10}

        self.__Ancestry = None
        self.__Background = None
        self.__Class = None
        self.__Size = None
        self.__Speed = 30
        self.__HitPoints = 0

        self.__Level = 0
        self.__ExperiencePoints = 0
        self.__KeyScore = None
        self.__ClassDC = None

        self.__armorClass = {"DexCap": None, "Proficiency": 0, "Item": 0, "Shield": 0}
        self.__armorProf = {"Unarmored": "Untrained", "Light": "Untrained", "Medium": "Untrained", "Heavy": "Untrained"}
        self.__attackProf = {"Unarmored": "Untrained", "Simple":"Untrained", "Martial":"Untrained"}

        self.__Saves = []
        self.__Skills = []
        self.__Melee = []
        self.__Range = []

        self.__Finished = False
        self.__buildNewCharacter()

    def __buildNewCharacter(self):
        for skill in SKILLSLIST:
            if len(skill) == 3:
                armor = True
            else:
                armor = False

            self.__Skills.append(Skill(skill[0], skill[1], self.__Level, self.__Scores.get(skill[1]), armor))

        for save in SAVES:
            self.__Saves.append(Skill(save[0], save[1], self.__Level, self.__Scores.get(save[1])))


    ### Class Section ###
    def getClass(self):
        return self.__Class

    def getAncestry(self):
        return self.__Ancestry

    def getSize(self):
        return self.__Size

    def getSpeed(self):
        return self.__Speed

    def setAncestry(self, value: Ancestry):
        self.__Ancestry = value

    def setSize(self, value):
        self.__Size = value

    def setSpeed(self, value):
        self.__Speed = value

    def setClass(self, value):
        self.__Class = value



    ### Armor Section ###

    def equipArmor(self, dexCap, type, item):
        self.__armorClass["DexCap"] = int(dexCap)
        self.__armorClass["Item"] = int(item)
        if type in self.__armorProf:
            proficiency = self.__armorProf[type]
        else:
            raise NameError("That is not a valid armor type: " + str(type))
        if self.__armorProf == "Untrained":
            self.__armorClass["Proficiency"] = 0
        else:
            self.__armorClass["Proficiency"] = PROFICIENCYLIST[proficiency] + self.__Level

    def equipShield(self, shield):
        self.__armorClass["Shield"] = int(shield)

    def unequipArmor(self):
        self.__armorClass["DexCap"] = None
        self.__armorClass["Item"] = 0
        if self.__armorProf["Unarmored"] == "Untrained":
            self.__armorClass["Proficiency"] = 0
        else:
            self.__armorClass["Proficiency"] = PROFICIENCYLIST[self.__armorProf["Unarmored"]] + self.__Level

    def getArmorClass(self):
        if self.__armorClass["DexCap"] is None:
            DexBonus = (self.__Scores["Dex"] - 10) // 2
        elif self.__armorClass["DexCap"] > (self.__Scores["Dex"] - 10) // 2:
            DexBonus = (self.__Scores["Dex"] - 10) // 2
        else:
            DexBonus = self.__armorClass["DexCap"]

        return 10 + DexBonus + self.__armorClass["Proficiency"] + self.__armorClass["Item"]

    def getArmorProf(self):
        return self.__armorProf

    ### Scores ###

    def getScore(self, score):
        if score not in self.__Scores:
            raise NameError("Score could not be found: '" + str(score) + "'")
        return self.__Scores.get(score)

    def setScore(self, score, newValue):
        if score in self.__Scores:
            self.__Scores[score] = newValue
        else:
            raise NameError(f"Attribute could not be found: '{score}'")
        if self.__Finished:
            self.__updateSheets()

    def setKeyScore(self, score):
        if score in self.__Scores:
            self.__KeyScore = score
        else:
            raise NameError(f"Attribute could not be found: '{score}'")

    def getKeyScore(self):
        return self.__KeyScore

    def printScores(self):
        for score in self.__Scores:
            print(score, ":{:>3}".format(self.__Scores.get(score)))

    def getFortitude(self):
        return self.__Saves[0]

    def getReflex(self):
        return self.__Saves[1]

    def getWill(self):
        return self.__Saves[2]

    ### Skills ###

    def printSkills(self):
        for skill in self.__Skills:
            print("{:<14}".format(str(skill.getSkill())) + ":{:>3}".format(str(skill.getBonus())))

    def printSaves(self):
        for save in self.__Saves:
            print("{:<10}".format(str(save.getSkill())) + ":{:>3}".format(str(save.getBonus())))

    def searchSkills(self, value):
        for skill in self.__Skills:
            if value == skill.getSkill():
                return skill
        return None

    def getClassDC(self):
        return self.__ClassDC

    def setClassDC(self, value):
        self.__ClassDC = value

    def getAttackProf(self):
        return self.__attackProf

    ### Level and XP ####

    def setHP(self):
        hp = ANCESTORS.get(self.getAncestry())[7]
        hp += CLASSES.get(self.getClass())[1] * self.getLevel()
        # TODO: Add feat Bonus Option
        self.__HitPoints = hp

    def getHP(self):
        return self.__HitPoints

    def levelUp(self):
        return  # TODO:

    def finished(self):
        self.__Finished = not self.__Finished
        self.__updateSheets()

    def getLevel(self):
        return self.__Level

    def setLevel(self, newValue):
        self.__Level = newValue

    def __updateSheets(self):
        for skill in self.__Skills:
            skill.setLevel(self.__Level)
            skill.setScoreValue(self.__Scores[skill.getScore()])
        for save in self.__Saves:
            save.setLevel(self.__Level)
            save.setScoreValue(self.__Scores[save.getScore()])
        self.setHP()

    def addXP(self, XP):
        self.__ExperiencePoints += XP
        if self.__ExperiencePoints > 1000:
            self.__ExperiencePoints -= 1000
            self.levelUp()

    ### Weapons ###
