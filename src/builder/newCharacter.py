from src.constants.classConstants import LEVELING
from data.characterData import CharacterData
from builder.setClass import setClass
from builder.setAncestory import chooseAncestry
from data.ancestry import Ancestry
from constants.constants import SCORELIST


def newCharacter_old():
    print("Building character... \n")
    character = CharacterData()
    ancestry = input("Ancestries:\n\tDwarf\n\tElf\n\tGnome\n\tGoblin\n\tHalfling\n\tHuman\nWhat is your character's ancestry? ").capitalize()
    #setAncestry(character, ancestry)
    charClass = input("Classes:\n\tAlchemist\n\tBarbarian\n\tBard\n\tChampion\n\tCleric\n\tDruid"
                      "\n\tFighter\n\tMonk\n\tRanger\n\tRogue\n\tSorcerer\n\tWizard\nWhat is your character class? ").capitalize()
    setClass(character, charClass)
    character.finished()
    print("\nfinished!")

    print("\n\nCharacter Stats\n")
    print(f"HP: {character.getHP()} \nSize: {character.getSize()} \nSpeed: {character.getSpeed()} \n")

    character.printScores()
    print()
    print(f"Class DC: {character.getClassDC().getBonus()}")
    print(f"ArmorClass: {character.getArmorClass()}\n")
    character.printSaves()
    print()
    character.printSkills()
    print()

def chooseScores(ancestry):
    usedList = [False, False, False, False, False, False]
    boosts = ancestry.getBoosts()
    for item in range(len(boosts)):
        if boosts[item] == "Free":
            accepted = False
            while not accepted:
                print("Scores:")
                for i in range(len(SCORELIST)):
                    print(f"\t{i + 1}: {SCORELIST[i]}")
                choice = input("Choose a Score to be boosted: ")
                try:
                    if not usedList[int(choice) - 1]:
                        choice = SCORELIST[int(choice) - 1]
                        accepted = True
                    else:
                        print("You cannot boost that Score!")
                except:
                    print("That is not a valid choice")
            boosts[item] = choice

        else:
            for i in range(len(SCORELIST)):
                if SCORELIST[i] == boosts[item]:
                    usedList[i] = True
            print(f"Boosted: {boosts[item]}")

def newCharacter():
    ancestry, name = chooseAncestry()
    ancestry = Ancestry(ancestry, name)
    print(f"Chosen ancestry: {ancestry.getAncestry()}")
    chooseScores(ancestry)
    print(ancestry.getAncestry(), ancestry.getBoosts())
    character = CharacterData(ancestry)
    print(character.getAncestry())
