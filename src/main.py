from builder.newCharacter import newCharacter
from data import characterData
import json
from data.characterData import CharacterData

'''
Tommy's review
Done: At start where is told me to pick a stat to increase, change Stat to Ability Score for consistent terminology
Done: An explanation of why that increase is happening would be nice
Done: When selecting what skills to be trained in, a notification of how many skills I can be trained in would be nice.
   Later GUI option, boxes to select which to be trained in
/help options to know what syntax is expected would be helpful


List Class skills already Trained in
Priority:
    Unittests (Always)
    Classes: Subgroups
    Backgrounds
    Ancenstry: Heritages
    Leveling
    Print Sheets
'''

if __name__ == '__main__':
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
    character.addWeapon("Melee", "Mace", "Strength", 1, 6, "Trained", "B", 0, 1, traits="Shove", descripton="This is the weapon descritption")
    character.printMeleeWeapons()
