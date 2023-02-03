import random
from reference.constants import ANCESTORS, SCORELIST
from import_functions.ancestries import ANCENTRIES

def chooseAncestry():
    sources = {}
    for item in ANCENTRIES:
        source = ANCENTRIES[item]["system"]["source"]['value']
        if "Lost Omens:" in source:
            temp = source.split(":")
            if temp[0] not in sources:
                sources[temp[0]] = {}
            sources[temp[0]][temp[1]] = ANCENTRIES[item]
        elif source not in sources:
            sources[source] = ANCENTRIES[item]

    listBooks(sources)
    selection = []
    resume = False
    selection = selectBooks(selection, sources)
    while not resume:
        print("\nYou selected: ")
        for book in selection:
            print(f"\t{book}")
        ans = input("Is that all (Y/N) or restart (R): ")
        if ans.lower() == "n" or ans.capitalize() == "no" or len(selection) == 0:
            listBooks(sources)
            selectBooks(selection, sources)
        elif ans.lower() == "y" or ans.lower() == "yes":
            resume = not resume
        elif ans.lower() == "r" or ans.lower() == "restart":
            selection = []
            listBooks(sources)
            selectBooks(selection, sources)
        else:
            print("Oops! That is not a valid answer!")

    choiceList = listCharacters(selection)
    choice = ""
    while resume:
        print("Which Ancestry do you want(#)? -d for description, -r for repeat")
        choice = input("Choice: ")
        if choice == "-r":
            listCharacters(selection)
        elif '-d' in choice:
            temp = choice.split(" ")
            if temp[0].isdigit() and int(temp[0]) in range(1, len(choiceList) + 1):
                print(f"\n\t{choiceList[int(temp[0]) - 1]}\n")
                print(f"{ANCENTRIES[choiceList[int(temp[0]) - 1]]['system']['description']['value']}\n")
        elif choice.isdigit() and int(choice) in range(1, len(choiceList) + 1):
            choice = ANCENTRIES[choiceList[int(choice) - 1]]
            resume = not resume
        else:
            print("That is not a valid response")
3


def listCharacters(selection):
    count = 1
    choiceList = []
    for book in selection:
        for item in ANCENTRIES:
            if ANCENTRIES[item]["system"]["source"]['value'] == book:
                print(f"{count}) {item}")
                choiceList.append(item)
                count += 1
    return choiceList


def listBooks(sources):
    count = 1
    print("\nWhich books are you playing with?")
    for source in sources:
        if "Lost Omens" in source:
            print(f"   {source}:")
            for book in sources[source]:
                print(f"{count})\t{book}")
                count += 1
            count -= 1
        else:
            print(f"{count}) {source}")
        count += 1


def selectBooks(selection, sources):
    resume = False
    print("Input # for book, 0 to continue, -r to repeat; One input at a time:")
    while not resume:
        ans = input("Number here: ")
        if ans == "-r":
            listBooks(sources)
        elif not ans.isdigit():
            print("That is not a valid response")
        elif int(ans) == 0:
            resume = True
        elif int(ans) == 1:
            selection.append("Pathfinder Lost Omens: The Mwangi Expanse")
        elif int(ans) == 2:
            selection.append("Pathfinder Lost Omens: Ancestry Guide")
        elif int(ans) == 3:
            selection.append("Pathfinder Lost Omens: Absalom, City of Lost Omens")
        elif int(ans) == 4:
            selection.append("Pathfinder Lost Omens: Impossible Lands")
        elif int(ans) == 5:
            selection.append("Pathfinder Lost Omens: Character Guide")
        elif int(ans) == 6:
            selection.append("Pathfinder Lost Omens: The Grand Bazaar")
        elif int(ans) == 7:
            selection.append("Pathfinder Guns & Gears")
        elif int(ans) == 8:
            selection.append("Pathfinder Advanced Player's Guide")
        elif int(ans) == 9:
            selection.append("Pathfinder Core Rulebook")
        elif int(ans) == 10:
            selection.append("Pathfinder #153: Life's Long Shadows")
        elif int(ans) == 11:
            selection.append("Pathfinder Book of the Dead")
        else:
            print("That is not a valid response")
    return selection


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