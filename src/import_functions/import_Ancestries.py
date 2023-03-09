import json

def buildAncestryJson(array, charJson):
    name = array[4]
    if "Heritage" in name:
        return buildHeritageJson(array, charJson)
    charJson[name] = {}
    setUpJson(charJson[name])

    description = ""
    extras = []
    index = 5
    resume = True


    while resume:
        # print(f"{index} {array[index]}")
        if array[index].startswith("trait") and len(charJson[name]["addLanguages"]) == 0:
            charJson[name]["trait"][array[index].split(": ")[1]] = ": ".join(array[index + 1].split(": ")[1:])
        if array[index].startswith("Source"):
            charJson[name]["source"] = array[index].removeprefix("Source").strip()
            index += 1
        if array[index].endswith("Mechanics"):
            charJson[name]["description"] = description
            charJson[name]["hp"] = array[index + 2]
        if charJson[name]["source"] != '' and charJson[name]["hp"] == '':
            description += f"{array[index]}\n".replace("Heading: ", "\t")
        if array[index] == "Heading:Size":
            charJson[name]["size"] = array[index + 1]
        if array[index] == "Heading:Speed":
            charJson[name]["speed"] = array[index + 1]
        if array[index] == "Heading:Ability Boosts":
            if "Two free" in array[index + 1]:
                charJson[name]["boosts"].append("Free")
                charJson[name]["boosts"].append("Free")
            else:
                count = 1
                while array[index + count] != "Heading:Ability Flaw(s)" and array[index + count] != "Heading:Languages":
                    charJson[name]["boosts"].append(array[index + count])
                    count += 1
        if array[index] == "Heading:Ability Flaw(s)":
            count = 1
            while array[index + count] != "Heading:Languages":
                charJson[name]["flaws"].append(array[index + count])
                count += 1
        if array[index] == "Heading:Languages":
            count = 1
            while not array[index + count].startswith("Additional"):
                charJson[name]["languages"].append(array[index + count])
                count += 1
        if array[index].startswith("Additional languages"):
            list1 = array[index].split(' ')
            for item in list1:
                if item.endswith(","):
                    charJson[name]["addLanguages"].append(item.strip(","))
            array.pop(index)
        if len(charJson[name]["addLanguages"]) != 0 and array[index] != "eof":
            extras.append(array[index])
        if array[index] != "eof":
            index += 1
        else:
            resume = False

    # https://2e.aonprd.com/Ancestries.aspx?ID=18
    # format Table
    charJson[name]["extras"] = parseExtras(extras)
    # file = open(f"{name}.json", mode="w")
    # print(f"{json.dumps(charJson[name], indent=2)}", file=file)
    # file.close()
    return json.dumps(charJson[name], indent=2)

# TODO:
def buildHeritageJson(array, charJson):
    ancestry = array[4].strip(")").split("(")[1].split(" ")[0]
    name = array[4].split("(")[0].strip()
    #print(f"{name}: {ancestry}")
    charJson[ancestry]["heritages"][name] = {}
    charJson[name] = {}
    charJson[name]["source"] = ""
    charJson[name]["description"] = ""
    charJson[ancestry]["heritages"][name]["short"] = ""
    charJson[ancestry]["heritages"][name]["shortSource"] = ""
    write = False
    description = ""
    index = 0
    while index < len(array):
        #print(array[index])
        if array[index].startswith(f"Heading:{ancestry}"):
            write = False
        if array[index].startswith("Source"):
            write = True
            if charJson[name]["source"] == "":
                charJson[name]["source"] = array[index].strip("Source ")
            else:
                charJson[ancestry]["heritages"][name]["shortSource"] = array[index].strip("Source ")
                description += f"See {ancestry} heritages.\n"
                charJson[name]["description"] = description
                description = ""
            index += 1
        if "eof" in array[index]:
            charJson[ancestry]["heritages"][name]["short"] = description
        if write and not array[index].startswith("Ancestry Page"):
            description += f"{array[index]}\n"
        index += 1


# TODO
def importHeritage(array, charJson):
    ancestry = array[1].split(" ")[0].split(":")[1]
    name = array[4]
    print(f"{ancestry}: {name}")
    item = {}
    item["feats"] = []
    item["source"] = ""
    item["description"] = ""
    index = 5
    while index < len(array):
        if array[index].startswith("Source") and item["source"] == "":
            item["source"] = array[index].strip("Source ")
        if array[index].startswith("Heading:Feats"):
            item["feats"] = array[index+1:len(array) - 1]
        print(array[index])

        index += 1
    print("\n\nCharacter")
    for temp in item:
        print(f"{temp}: {item[temp]}")
    charJson[ancestry]["heritages"][name] = item

def parseExtras(extras):
    newDict = {}
    if len(extras) != 0:
        section = ""
        index = 0
        while index < len(extras):
            #print(extras[index])
            if extras[index].startswith("Heading") and len(extras[index].split(":")[1].strip()) != 0:
                nextline = extras[index].split(":")[1].strip()
            #print(f"{nextline} : {nextline in newDict}")
                if nextline in newDict or nextline.startswith("Table"):
                    ability, index = buildAbility(extras[index:], index)
                    newDict[section]["ability"] = ability
                else:
                    section = nextline
                    newDict[section] = {}
                    newDict[section]["description"] = ""
            else:
                newDict[section]["description"] += f"{extras[index]}\n"
            index += 1
    #print(json.dumps(newDict, indent=2))
    return newDict

def buildAbility(abilities, prev):
    abilityDict = {}
    if abilities[0].startswith("Heading"):
        return abilityDict, prev + 1
    ability = abilities.pop(0).split(":")[1].strip()
    abilityDict[ability] = {}
    abilityDict[ability]["description"] = ""
    if ability.startswith("Table"):
        index = 1
        while index < len(abilities):
            abilityDict[ability]["description"] += abilities[index]
            index += 1
    else:
        abilityDict[ability]["trait"] = {}
        index = 0
        while index < len(abilities):
            #print(f"{abilities[index]}")
            if abilities[index].startswith("trait"):
                abilityDict[ability]["trait"][abilities[index].split(': ')[1]] = abilities[index + 1].split(": ")[1]
            elif abilities[index].startswith("Heading"):
                index += 1
                break
            elif abilities[index].startswith("Body:"):
                abilityDict[ability]["description"] += abilities[index].split(":")[1]
            else:
                abilityDict[ability]["description"] += abilities[index]
            index += 1
    return abilityDict, index + prev

def setUpJson(param):
    param["source"] = ""
    param["trait"] = {}
    param["description"] = ''
    param["hp"] = ''
    param["size"] = ''
    param["speed"] = ''
    param["boosts"] = []
    param["flaws"] = []
    param["languages"] = []
    param["addLanguages"] = []
    param["extras"] = {}
    param["heritages"] = {}