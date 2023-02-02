import random

DCLEVELS = [14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 38, 39, 40, 42, 44, 46, 48, 50]

INCOME_FAIL = [[1, 0, 0], [2, 0, 0], [4, 0, 0], [8, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0],
               [0, 6, 0], [0, 7, 0], [0, 8, 0], [0, 9, 0], [0, 0, 1], [0, 5, 1], [0, 0, 2], [0, 5, 2], [0, 0, 3],
               [0, 0, 4], [0, 0, 6], [0, 0, 8], [0, 0, 0]]
INCOME_TRAINED = [[5, 0, 0], [0, 2, 0], [0, 3, 0], [0, 5, 0], [0, 7, 0], [0, 9, 0], [0, 5, 1], [0, 0, 2], [0, 5, 2],
               [0, 0, 3], [0, 0, 4], [0, 0, 5], [0, 0, 6], [0, 0, 7], [0, 0, 8], [0, 0, 10], [0, 0, 13], [0, 0, 15],
               [0, 0, 20], [0, 0, 30], [0, 0, 40], [0, 0, 50]]
INCOME_EXPERT = [[5, 0, 0], [0, 2, 0], [0, 3, 0], [0, 5, 0], [0, 8, 0], [0, 0, 1], [0, 0, 2], [0, 5, 2], [0, 0, 3],
               [0, 0, 4], [0, 0, 5], [0, 0, 6], [0, 0, 8], [0, 0, 10], [0, 0, 15], [0, 0, 20], [0, 0, 25], [0, 0, 30],
               [0, 0, 45], [0, 0, 60], [0, 0, 75], [0, 0, 90]]
INCOME_MASTER = [[5, 0, 0], [0, 2, 0], [0, 3, 0], [0, 5, 0], [0, 8, 0], [0, 0, 1], [0, 0, 2], [0, 5, 2], [0, 0, 3],
               [0, 0, 4], [0, 0, 6], [0, 0, 8], [0, 0, 10], [0, 0, 15], [0, 0, 20], [0, 0, 28], [0, 0, 36], [0, 0, 45],
               [0, 0, 70], [0, 0, 100], [0, 0, 150], [0, 0, 175]]
INCOME_LEGENDARY = [[5, 0, 0], [0, 2, 0], [0, 3, 0], [0, 5, 0], [0, 8, 0], [0, 0, 1], [0, 0, 2], [0, 5, 2], [0, 0, 3],
               [0, 0, 4], [0, 0, 6], [0, 0, 8], [0, 0, 10], [0, 0, 15], [0, 0, 20], [0, 0, 28], [0, 0, 40], [0, 0, 55],
               [0, 0, 90], [0, 0, 130], [0, 0, 200], [0, 0, 300]]

def getDC(level):
    return DCLEVELS[level]

def rollD20(profBonus):
    dice = random.randint(1,20)
    if (dice == 1):
        return "Crit Fail!"
    elif (dice == 20):
        return "Crit Success!"
    else:
        return profBonus + dice

def getIncome(proficiency, taskLevel, dice):
    dc = getDC(taskLevel)
    result = 0
    if dice == "Crit Fail!":
        return [0, 0, 0]
    elif dice == "Crit Success!":
        dice = dc + 10

    if proficiency == "Trained":
        income = INCOME_TRAINED
    elif proficiency == "Expert":
        income = INCOME_EXPERT
    elif proficiency == "Master":
        income = INCOME_MASTER
    elif proficiency == "Legendary":
        income = INCOME_LEGENDARY

    if result == 22:
        return income[result]
    elif dice > dc + 10:
        return income[22]
    elif dice > dc:
        return income[taskLevel]
    else:
        return INCOME_FAIL[taskLevel]

def getShipIncome(days, partyLevel):
    shipProf = "Trained"
    shipBonus = 8
    gold = 0
    silver = 0
    copper = 0
    for i in range(days):
        level = random.randint(partyLevel - 2, partyLevel + 2)
        income = getIncome(shipProf, level, rollD20(shipBonus))
        gold += income[2]
        silver += income[1]
        copper += income[0]
    return [copper, silver, gold]


if __name__ == '__main__':
    partySize = 5
    partyLevel = 10
    days = 200
    income = getShipIncome(days, partyLevel)

    print(f"gold: {income[2] * partySize}\nsilver: {income[1] * partySize}\ncopper: {income[0] * partySize}")
