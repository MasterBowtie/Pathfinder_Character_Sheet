from src.reference.classConstants import LEVELING
from data.characterData import CharacterData
from builder.setClass import setClass
from builder.setAncestory import setAncestry

def newCharacter():
    print("Building character... \n")
    character = CharacterData()
    ancestry = input("Ancestries:\n\tDwarf\n\tElf\n\tGnome\n\tGoblin\n\tHalfling\n\tHuman\nWhat is your character's ancestry? ").capitalize()
    setAncestry(character, ancestry)
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