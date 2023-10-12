# from data.skill import Skill
# from constants.constants import SKILLSLIST, SAVES, PROFICIENCYLIST, SCORELIST
# from constants.classConstants import CLASSES
# from data.ancestry import Ancestry
import json

PROFICIENCIES = ['untrained', 'trained', 'expert', 'master', 'legendary']
WEAPON = {
        "name": {},
        "to_hit": {
          "score": None,
          "proficiency": "untrained",
          "item_bonus": 0
        },
        "damage": {
          "special": 0,
          "dice": {
            "number": 0,
            "size": 0
          },
          "type": {
            "blunt": 0,
            "piercing": 0,
            "slashing": 0
          },
          "weapon_special": 0,
          "other": {},
          "traits": {}
        }
      }

class CharacterData:
    def __init__(self):
        self.__character = None
        file = open("characterSheet.json")
        self.__character = json.load(file)
        file.close()
        #print(json.dumps(self.__character, indent=2))

        # self.__strength = self.__character["page0"]["scores"]["strength"]
        # self.__dexterity = self.__character["page0"]["scores"]["dexterity"]
        # self.__constitution = self.__character["page0"]["scores"]["constitution"]
        # self.__intelligence = self.__character["page0"]["scores"]["intelligence"]
        # self.__wisdom = self.__character["page0"]["scores"]["wisdom"]
        # self.__charisma = self.__character["page0"]["scores"]["charisma"]

    ### Class Section ###
    def getClass(self):
        return self.__character["page0"]["description"]["class"]

    def getAncestry(self):
        return self.__character["page0"]["description"]["ancestry"]

    def setClass(self, value):
        if value is str:
            self.__character["page0"]["description"]["class"] = value
        else:
            print("This is not a valid input")

    def getProficiency(self, value):
        if value == "untrained":
            return 0
        if value == "trained":
            return 2 + self.__character["page0"]["description"]["level"]
        if value == "expert":
            return 4 + self.__character["page0"]["description"]["level"]
        if value == "master":
            return 6 + self.__character["page0"]["description"]["level"]
        if value == "legendary":
            return 8 + self.__character["page0"]["description"]["level"]
        return -1

    ### Armor Section ###
    def equipArmor(self):
        pass

    def equipShield(self):
        pass

    def unequipArmor(self):
        pass

    def getArmorClass(self):
        pass

    def getArmorProf(self):
        pass

    ### Scores ###
    def getScore(self, score):
        if score not in self.__character["page0"]["scores"]:
            raise NameError("Score could not be found: '" + str(score) + "'")
        return self.__character["page0"]["scores"][score]

    def setScore(self, score, newValue):
        score = score.lower()
        if score in self.__character["page0"]["scores"]:
            self.__character["page0"]["scores"][score] = newValue
        else:
            raise NameError(f"Attribute could not be found: '{score}'")

    def printScores(self):
        for score in self.__character["page0"]["scores"]:
            print(f"{score[0:3].capitalize():>4}: {self.__character['page0']['scores'][score]}")

    def printSaves(self):
        for save in self.__character["page0"]["saving_throws"]:
            bonus = self.getSave(save)
            print(f"{save.capitalize(): >10}: {bonus}")

    def getSave(self, save):
        score = (self.__character["page0"]["scores"][self.__character["page0"]["saving_throws"][save]["score"]] - 10) // 2
        # print(f"Score Modifier: {score}")
        proficiency = self.getProficiency(self.__character["page0"]["saving_throws"][save]["proficiency"])
        # print(f"Proficency Bonus: {self.__character['page0']['saving_throws'][save]['proficiency']} -> {proficiency}")
        bonus = self.__character["page0"]["saving_throws"][save]["item_bonus"]
        # print(f"Item Bonus: {self.__character['page0']['saving_throws'][save]['item_bonus']}")
        return score + proficiency + bonus

    def setSaveProficiency(self, save, proficiency):
        save = save.lower()
        proficiency = proficiency.lower()
        if save in self.__character["page0"]["saving_throws"] and proficiency in PROFICIENCIES:
            self.__character["page0"]["saving_throws"][save]["proficiency"] = proficiency




    ### Skills ###
    def getSkill(self, skill):
        score = (self.__character["page0"]["scores"][
                     self.__character["page0"]["skills"][skill]["score"]] - 10) // 2
        # print(f"Score Modifier: {score}")
        proficiency = self.getProficiency(self.__character["page0"]["skills"][skill]["proficiency"])
        # print(f"Proficency Bonus: {self.__character['page0']['saving_throws'][save]['proficiency']} -> {proficiency}")
        bonus = self.__character["page0"]["skills"][skill]["item_bonus"]
        # print(f"Item Bonus: {self.__character['page0']['saving_throws'][save]['item_bonus']}")
        return score + proficiency + bonus

    def setSkillProficiency(self, skill, proficiency):
        skill = skill.lower()
        proficiency = proficiency.lower()
        if skill in self.__character["page0"]["skills"] and proficiency in PROFICIENCIES:
            self.__character["page0"]["skills"][skill]["proficiency"] = proficiency

    def printSkills(self):
        for skill in self.__character['page0']['skills']:
            if "lore" in skill:
                string = skill[:-1].capitalize() + "(" + self.__character['page0']['skills'][skill]['topic'] + ")"

                print(f"{string: >20}: {self.getSkill(skill)}")
            else:
                print(f"{skill.capitalize(): >20}: {self.getSkill(skill)}")


    def getClassDC(self):
        return self.__character["page0"]["class_dc"]


    def setClassDCAbility(self, value):
        # TODO:
        pass


    ### Level and XP ####
    def addHP(self, value):
        self.__character["page0"]["hit_points"]["current"] += value


    def getCurrentHP(self):
        return self.__character["page0"]["hit_points"]["current"]

    def getMaxHP(self):
        return self.__character["page0"]["hit_points"]["max"]

    def levelUp(self):
        pass
        #TODO:

    def getLevel(self):
        return self.__character["page0"]["description"]["level"]

    def addXP(self, XP):
        self.__character["page0"]["description"]["experience_points"] += XP
        if self.__character["page0"]["description"]["experience_points"] > 1000:
            self.__character["page0"]["description"]["experience_points"] -= 1000
            self.levelUp()

    ### Weapons ###
if __name__ == "__main__":
    character = CharacterData()
    character.setScore("strength", 18)
    character.setScore("dexterity", 14)
    character.setScore("constitution", 16)
    character.setScore("intelligence", 10)
    character.setScore("wisdom", 12)
    character.setScore("charisma", 8)
    character.setSaveProficiency("fortitude", "expert")
    character.setSkillProficiency("thievery", "EXPERT")
    character.printScores()
    print()
    character.printSaves()
    print()
    character.printSkills()