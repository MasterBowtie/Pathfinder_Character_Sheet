from src.constants.constants import PROFICIENCIES, WEAPON, SCORELIST
import copy
import json


class CharacterData:
    def __init__(self):
        self.__character = None
        file = open("constants/characterSheet.json")
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
        # TODO:
        pass

    def equipShield(self):
        # TODO:
        pass

    def unequipArmor(self):
        # TODO:
        pass

    def getArmorClass(self):
        # TODO:
        pass

    def getArmorProf(self):
        # TODO:
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

    def setWeaponTypeProficiency(self, weapon_type, proficiency):
        if proficiency in PROFICIENCIES:
            if weapon_type in self.__character["page0"]["weapon_proficiencies"]:
                self.__character["page0"]["weapon_proficiencies"][weapon_type] = proficiency
            elif weapon_type == self.__character["page0"]["weapon_proficiencies"]["other0"]["name"]:
                self.__character["page0"]["weapon_proficiencies"]["other0"]["proficiency"] = proficiency
            elif weapon_type == self.__character["page0"]["weapon_proficiencies"]["other1"]["name"]:
                self.__character["page0"]["weapon_proficiencies"]["other1"]["proficiency"] = proficiency

    def addWeapon(self, attack_type, name, score, dice_number, dice_size, proficiency, weapon_types, item_bonus=0, bulk=0, weapon_special=0, traits="", descripton=""):
        weapon = copy.deepcopy(WEAPON)
        weapon["name"] = name
        if score.lower() in SCORELIST:
            weapon["to_hit"]["score"] = score.lower()
        if proficiency.lower() in PROFICIENCIES:
            weapon["to_hit"]["proficiency"] = proficiency.lower()
        weapon["to_hit"]["item_Bonus"] = item_bonus
        weapon["damage"]["dice"]["number"] = dice_number
        weapon["damage"]["dice"]["size"] = dice_size
        weapon["damage"]["weapon_special"] = weapon_special
        weapon_types = weapon_types.split("/")
        for w_type in weapon_types:
            if w_type in weapon["damage"]["type"]:
                weapon["damage"]["type"][w_type] = 1
        weapon["attack_type"] = attack_type
        weapon["bulk"] = bulk
        weapon["traits"] = traits
        weapon["description"] = descripton
        if attack_type == "melee":
            self.__character['page0']['melee_strikes'].append(weapon)
        if attack_type == "ranged":
            self.__character['page0']['ranged_strikes'].append(weapon)
        self.__character["page0"]["melee_strikes"].append(weapon)

    def printMeleeWeapons(self):
        # print(json.dumps(self.__character["page0"]["melee_strikes"], indent=2))
        for weapon in range(len(self.__character["page0"]["melee_strikes"])):
            name = self.__character["page0"]["melee_strikes"][weapon]["name"]
            score = (self.__character["page0"]["scores"][self.__character["page0"]["melee_strikes"][weapon]["to_hit"]["score"]] - 10) // 2
            proficiency = self.getProficiency(self.__character["page0"]["melee_strikes"][weapon]["to_hit"]["proficiency"])
            item_bonus = self.__character["page0"]["melee_strikes"][weapon]["to_hit"]["item_bonus"]
            toHit = score + proficiency + item_bonus
            damage = f"{self.__character['page0']['melee_strikes'][weapon]['damage']['dice']['number']}d{self.__character['page0']['melee_strikes'][weapon]['damage']['dice']['size']}"

            print(f"{name}: {toHit} {damage}")
