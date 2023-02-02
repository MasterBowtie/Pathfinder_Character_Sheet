import random
from reference.constants import ANCESTORS, SCORELIST
from import_functions.ancestries_constants import ANCENTRIES



def setAncestry(character, choice, randomize=False):
    ancestor = None
    
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


def pickScores(character, count, usedList):
    print(f"You get to choose {count} Ability boosts")
    while count > 0:
        stat = input("Ability Scores:\n\tStr\n\tDex\n\tCon\n\tInt\n\tWis\n\tCha\nWhich Ability Score do you want to increase? ").capitalize()
        #TODO:Set up for full name
        if stat in SCORELIST and not usedList[SCORELIST.index(stat)]:
            character.setScore(stat, character.getScore(stat) + 2)
            usedList[SCORELIST.index(stat)] = True
            count -= 1
        else:
            print("That stat is unable to be used")


def randomizeScores(character, count, usedList):
    while count > 0:
        stat = SCORELIST[random.randint(0,len(SCORELIST) - 1)]
        if stat in SCORELIST and not usedList[SCORELIST.index(stat)]:
            character.setScore(stat, character.getScore(stat) + 2)
            usedList[SCORELIST.index(stat)] = True
            count -= 1
            print(f"Picked Score: {stat}")