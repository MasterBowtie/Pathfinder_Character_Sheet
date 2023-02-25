from src.reference.classConstants import LEVELING
from data.characterData import CharacterData
from builder.setClass import setClass
from builder.newCharacter import newCharacter

def printLevelChart():
    num = 0
    print("Alchemist Leveling Chart")
    for level in LEVELING.get("Alchemist"):
        num += 1
        itemList = "\t" + str(num) + ": " + ', '.join(level)
        print(itemList)

'''
Tommy's review
Done: At start where is told me to pick a stat to increase, change Stat to Ability Score for consistent terminology
Done: An explanation of why that increase is happening would be nice
Done: When selecting what skills to be trained in, a notification of how many skills I can be trained in would be nice.
   Later GUI option, boxes to select which to be trained in
/help options to know what syntax is expected would be helpful
'''

'''
List Class skills already Trained in
Priority:
    Unittests (Always)
    Classes: Subgroups
    Backgrounds
    Ancenstry: Sub-races
    Leveling
    Print Sheets
'''

if __name__ == '__main__':
    newCharacter()
    pass
