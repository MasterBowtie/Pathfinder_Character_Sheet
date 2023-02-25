from src.reference.classConstants import LEVELING
from data.characterData import CharacterData
from builder.setClass import setClass
from builder.setAncestory import chooseAncestry
from data.ancestry import Ancestry
from reference.constants import SCORELIST


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
    # TODO: fill Free scores
    usedList = [False, False, False, False, False, False]
    for item in range(len(ancestry["boosts"])):
        if ancestry["boosts"][item] == "Free":
            accepted = False
            while not accepted:
                print("Scores:")
                for i in range(len(SCORELIST)):
                    print(f"\t{i + 1}: {SCORELIST[i]}")
                choice = input("Chose a Score: ")
                try:
                    if not usedList[int(choice)]:
                        choice = SCORELIST[int(choice)]
                        accepted = True
                except:
                    print("That is not a valid choice")
            ancestry["boosts"][item] = choice

        else:
            for i in range(len(SCORELIST)):
                if SCORELIST[i] == ancestry["boosts"][item]:
                    usedList[i] = True
            print(ancestry["boosts"][item])

'''
   
        for item in ANCESTORS:
            if choice == item:
                ancestor = item
        if ancestor != None:
            print(f"{ancestor} has:", end="\n\t")
            character.setAncestry(ancestor)
            info = ANCESTORS.get(ancestor)
            usedList = [False, False, False, False, False, False]

            string = []
            for i in range(len(SCORELIST)):
                if info[i] > 0:
                    character.setScore(SCORELIST[i], character.getScore(SCORELIST[i]) + info[i])
                    usedList[i] = True
                    string.append(f"{SCORELIST[i]} Boost")
                elif info[i] < 0:
                    character.setScore(SCORELIST[i], character.getScore(SCORELIST[i]) + info[i])
                    string.append(f"{SCORELIST[i]} Flaw")
            string = '\n\t'.join(string)
            print(string)

            if randomize:
                randomizeScores(character, info[6], usedList)
            else:
                pickScores(character, info[6], usedList)

            character.setSize(info[8])
            character.setSpeed(info[9])

        else:
            raise NameError("That is not a valid ancestry")
'''

def newCharacter():
    character = CharacterData()
    ancestry, name = chooseAncestry()
    ancestry = Ancestry(ancestry, name)
    print("Chosen ancestry:")
    chooseScores(ancestry)
    print(ancestry.getAncestry(), ancestry.getSize())
    character.setAncestry(ancestry)