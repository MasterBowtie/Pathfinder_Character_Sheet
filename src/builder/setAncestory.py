import random
from src.constants.constants import SCORELIST
from src.constants.ancestries import ANCESTRIES

def chooseAncestry():
    sources = []
    for item in ANCESTRIES:
        if item != "Versatile":
            source = ANCESTRIES[item]["source"].split("pg")[0]
            if source not in sources:
                sources.append(source)
    listBooks(sources)
    resume = False
    selection = []
    selectBooks(sources, selection)
    while not resume:
        print("\nYou selected: ")
        for book in selection:
            print(f"\t{book}")
        ans = input("Is that all (Y/N) or restart (R): ")
        if ans.lower() == "n" or ans.capitalize() == "no" or len(selection) == 0:
            listBooks(sources)
            selectBooks(sources, selection)
        elif ans.lower() == "y" or ans.lower() == "yes":
            resume = not resume
        elif ans.lower() == "r" or ans.lower() == "restart":
            listBooks(sources)
            selection = []
            selectBooks(sources, selection)
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

                print(f"\n{choiceList[int(temp[0]) - 1]}")
                giveDescription(ANCESTRIES[choiceList[int(temp[0]) - 1]])

        elif choice.isdigit() and int(choice) in range(1, len(choiceList) + 1):
            name = choiceList[int(choice) - 1]
            choice = ANCESTRIES[choiceList[int(choice) - 1]]
            resume = not resume
        else:
            print("That is not a valid response")
    return choice, name



def giveDescription(choice):
    for item in choice:
        if type(choice[item]) == dict or type(choice[item]) == list:
            print(f"{item.capitalize()}:")
            for item2 in choice[item]:
                print(f"\t{item2}")
            print()
        else:
            string = choice[item].replace("Heading:", "\t")
            print(f"{item.capitalize()}: {string}")
    print()


def listCharacters(selection):
    count = 1
    choiceList = []
    for book in selection:
        for item in ANCESTRIES:
            if item != "Versatile" and ANCESTRIES[item]["source"].split("pg")[0] == book:
                print(f"{count}) {item}")
                choiceList.append(item)
                count += 1
    return choiceList

def listBooks(sources):
    count = 1
    for source in sources:
        print(f"{count}) {source}")
        count += 1


def selectBooks(sources, selection):
    resume = False
    print("Input # for book, 0 to continue, -r to repeat; One input at a time:")
    while not resume:
        ans = input("Number here: ")
        if "-r" in ans:
            listBooks(sources)
            continue
        try:
            ans = int(ans)
            if ans == 0:
                resume = True
            elif 0 < ans < len(sources) + 1:
                selection.append(sources[ans - 1])
            else:
                raise IndexError
        except:
            print("That is not a valid response")
    return selection

'''
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
'''
