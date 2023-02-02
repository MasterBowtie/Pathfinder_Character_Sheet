import random

from reference.constants import SKILLSLIST
from reference.classConstants import CLASSES

from data.skill import Skill


# TODO: set up for Sorcerer Bloodlines, Rogue Racket, Fighter Skill, Druidic Order,
def setClass(character, selected, randomize=False):
    gameClass = None
    for item in CLASSES:
        if selected == item:
            gameClass = item
    if gameClass == None:
        print(f"\"{selected}\" is not an available class")
        return False
    else:
        info = CLASSES.get(gameClass)

#    if selected == 'Sorcerer':
#        info = selectBloodline(info, randomize)
#    elif selected == 'Rogue':
#        info = selectRacket(info, randomize)
    if selected == 'Fighter':
        info = selectSkill(info, randomize)
#    elif selected == 'Druid':
#        info = selectOrder(info, randomize)

    character.setLevel(1)
    character.setClass(selected)


    if len(info[0]) == 1:
        score = info[0][0]
    elif randomize:
        score = info[0][random.randint(0,len(info[0]) - 1)]
    else:
        score = input(f"Which key Score do you want ({','.join(info[0])})? ").capitalize()
    character.setKeyScore(score)
    character.setScore(score, character.getScore(score) + 2)
    skill = character.searchSkills('Perception')
    skill.setProficiency(info[2])
    character.getFortitude().setProficiency(info[3][0])
    character.getReflex().setProficiency(info[3][1])
    character.getWill().setProficiency(info[3][2])

    if randomize:
        randomizeSkills(character, info)
    else:
        print(f"{selected}s are Trained in: ", end="\n\t")
        pickSkills(character, info)

    attackProf = character.getAttackProf()
    attackProf["Unarmed"] = info[5][0]
    attackProf["Simple"] = info[5][1]
    attackProf["Martial"] = info[5][2]
    for prof in info[5][3]:
        attackProf[prof] = info[5][3][prof]

    armorProf = character.getArmorProf()
    armorProf["Unarmored"] = info[6][0]
    armorProf["Light"] = info[6][1]
    armorProf["Medium"] = info[6][2]
    armorProf["Heavy"] = info[6][3]


    character.setClassDC(Skill("Class DC", score, character.getLevel(), character.getScore(score), proficiency="Trained"))

    return True

#TODO User accessibility: show FREE skill count
'''
    for classSkill in classInfo[4]:
        if classSkill == 'FREE':
            classSkill = str(input("What skill would you like to train in? ").capitalize())
        if classSkill.split()[0] == "Lore" and character.searchSkills("Lore") != None:
            skill = character.searchSkills("Lore")
            skill.setSkill(classSkill)

        skill = character.searchSkills(classSkill)

        while skill == None or skill.getProficiency() != "Untrained":
            classSkill = str(input("Cannot use that Skill, pick an alternate: ").capitalize())
            skill = character.searchSkills(classSkill)
        skill.setProficiency('Trained')

    intMod = (character.getScore('Int') - 10) // 2
'''

def pickSkills(character, classInfo):
    skillCount = (character.getScore('Int') - 10) // 2
    string = []
    for classSkill in classInfo[4]:
        if classSkill == 'FREE':
            skillCount += 1
        else:
            skill = character.searchSkills(classSkill)
            skill.setProficiency('Trained')
            string.append(skill.getSkill())
    print("\n\t".join(string))

    print(f"You can choose {skillCount} skills to be Trained in")
    while skillCount > 0:
        classSkill = str(input("What skill would you like to train in? ").capitalize())
        if classSkill.split()[0] == "Lore" and character.searchSkills("Lore") != None:
            skill = character.searchSkills("Lore")
            skill.setSkill(classSkill)

        skill = character.searchSkills(classSkill)

        while skill == None or skill.getProficiency() != 'Untrained':
            classSkill = str(input("Cannot use that Skill, pick an alternate: ").capitalize())
            skill = character.searchSkills(classSkill)
        skill.setProficiency('Trained')
        skillCount -= 1


def randomizeSkills(character, classInfo):
    skillCount = (character.getScore('Int') - 10) // 2
    for classSkill in classInfo[4]:
        if classSkill == 'FREE':
            skillCount += 1
        else:
            skill = character.searchSkills(classSkill)
            skill.setProficiency('Trained')
            print(f"Trained in: {skill.getSkill()}")

    print(f"Randomly picking {skillCount} skills to Train in")

    while skillCount > 0:
        classSkill = SKILLSLIST[random.randint(0, len(SKILLSLIST) - 1)][0]
        print(classSkill)
        if classSkill.split()[0] == "Lore" and character.searchSkills("Lore") != None:
            skill = character.searchSkills("Lore")
            skill.setSkill(classSkill)

        skill = character.searchSkills(classSkill)

        while skill == None or skill.getProficiency() != 'Untrained':
            classSkill = SKILLSLIST[random.randint(0, len(SKILLSLIST) - 1)][0]
            skill = character.searchSkills(classSkill)
        skill.setProficiency('Trained')
        print(f"Trained in: {skill.getSkill()}")
        skillCount -= 1

'''
    for classSkill in classInfo[4]:
        if classSkill == 'FREE':
            classSkill = SKILLSLIST[random.randint(0,len(SKILLSLIST) - 1)][0]
            print(classSkill)

        skill = character.searchSkills(classSkill)

        while skill == None or skill.getProficiency() != "Untrained":
            classSkill = SKILLSLIST[random.randint(0,len(SKILLSLIST) - 1)][0]
            print(f"ReRoll: {classSkill}")
            skill = character.searchSkills(classSkill)

        skill.setProficiency('Trained')

    intMod = (character.getScore('Int') - 10) // 2
    while intMod > 0:
        classSkill = SKILLSLIST[random.randint(0,len(SKILLSLIST) - 1)][0]
        print(classSkill)
        skill = character.searchSkills(classSkill)

        while skill == None or skill.getProficiency() != 'Untrained':
            classSkill = SKILLSLIST[random.randint(0,len(SKILLSLIST) - 1)][0]
            print(f"ReRoll: {classSkill}")
            skill = character.searchSkills(classSkill)

        skill.setProficiency('Trained')
        intMod -= 1
'''

def selectSkill(info, randomized):
    valid = False
    if randomized:
        pick = random.choice(['Acrobatics', 'Athletics'])
        info[4].append(pick)
        print(f"Fighter Skill: {pick}")
    else:
        while not valid:
            response = input("Which skill do you want to be trained in; Acrobatics or Athletics? ").capitalize()
            if response == 'Acrobatics' or response == 'Athletics':
                info[4].insert(0,response)
                valid = True
    return info
