import json
import sys
import requests

def __buildJson(array, charJson):
    array.append("eof")

    name = array[0]
    if "Heritage" in name:
        raise ImportError
    charJson[name] = {}
    __setUpJson(charJson[name])


    description = ""
    extras = []
    index = 0
    resume = True
    while resume:
        if "class=\"trait\"" in array[index]:
            list1 = array[index].split("\"")
            charJson[name]["trait"][list1[1]] = list1[5]
        if array[index] == "Source":
            charJson[name]["source"] = array[index + 1]
            array[index + 1] = "Description"
            index += 1
        if array[index].endswith("Mechanics"):
            charJson[name]["description"] = description
            charJson[name]["hp"] = array[index + 2]
        if charJson[name]["source"] != '' and charJson[name]["hp"] == '':
            description += f"{array[index]}\n"
        if array[index] == "Heading: Size":
            charJson[name]["size"] = array[index + 1]
        if array[index] == "Heading: Speed":
            charJson[name]["speed"] = array[index + 1]
        if array[index] == "Heading: Ability Boosts":
            if "Two free" in array[index + 1]:
                charJson[name]["boosts"].append("Free")
                charJson[name]["boosts"].append("Free")
            else:
                count = 1
                while array[index + count] != "Heading: Ability Flaw(s)":
                    charJson[name]["boosts"].append(array[index + count])
                    count += 1
        if array[index] == "Heading: Ability Flaw(s)":
            count = 1
            while array[index + count] != "Heading: Languages":
                charJson[name]["flaws"].append(array[index + count])
                count += 1
        if array[index] == "Heading: Languages":
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

        if len(charJson[name]["addLanguages"]) != 0 and array[index] != "eof" :
            extras.append(array[index])

        if array[index] != "eof":
            index += 1
        else:
            resume = False

    # https://2e.aonprd.com/Ancestries.aspx?ID=18
    # format Table
    if len(extras) != 0:
        section = ""
        for line in extras:
            if line.startswith("Heading"):
                section = line.split(":")[1]
                charJson[name]["extras"][section] = ""
            else:
                charJson[name]["extras"][section] += f"{line}\n"

    print(f"{json.dumps(charJson[name], indent=2)} {name} ")

# \u2013 == -
# \u2011 == -
# \u2014 == -
# \u2019 == '
def discectHTML(html):
    html = html.replace("\u2013", "-").replace("\u2011", "-").replace("\u2014", "-").replace("\u2019", "'")
    file = html.split("\n")
    write = False
    file2 = []

    # filter lines...
    for line in file:
        if "id=\"main\"" in line:
            write = True
        if write and "</div>" in line:
            write = False
        if "" != line.strip() and write:
            file2.append(line.strip())

    string = ""
    for line in file2:
        line = line.replace("<span", "\n<span").replace("</span>", "\n</span>\n").replace("<li>", "\n\t- ")\
            .replace("alt=", "\nalt=>").replace("<b", "\n<b").replace("</b>", "</b>\n")\
            .replace("</h3>", "<split>\n").replace("</h2>", "<split>\n").replace("</h1>", "<split>\n") \
            .replace("<h1", "\n<split>Heading:<").replace("<h2", "\n<split>Heading: <").replace("&nbsp;", "")
        string += line
    file = string.split("<split>")

    newText = ""
    for line in file:
        write = True
        for char in line:
            if char == "<":
                write = False
            if write:
                newText += char
            if char == ">":
                write = True
        newText += "\n"
    file = newText.split("\n")

    count = 0
    found = False
    while count < len(file):
        if len(file[count]) == 0:
            file.pop(count)
        elif "src=" in file[count]:
            found = True
            file.pop(count)
        elif not found:
            file.pop(count)
        else:
            #print(f"{count} {file[count]}")
            count += 1
    return file


def __setUpJson(param):
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



# Error on
# https://2e.aonprd.com/Ancestries.aspx?ID=15
# https://2e.aonprd.com/Ancestries.aspx?ID=18
# https://2e.aonprd.com/Ancestries.aspx?ID=27
# https://2e.aonprd.com/Ancestries.aspx?ID=38
# https://2e.aonprd.com/Ancestries.aspx?ID=42
# https://2e.aonprd.com/Ancestries.aspx?ID=48
# https://2e.aonprd.com/Ancestries.aspx?ID=49
# https://2e.aonprd.com/Ancestries.aspx?ID=53
# https://2e.aonprd.com/Ancestries.aspx?ID=56

if __name__ == "__main__":
    debug = True
    baseURL = "https://2e.aonprd.com/"
    accepted = []
    failed = []
    jsonFile = {}
    if debug:
        count = 1
        target = 19
    else:
        count = 1
        target = 100

    while count < target:
        url = f"Ancestries.aspx?ID={count}"
        try:
            response = requests.get(f"{baseURL}{url}")
            if not response.ok:
                failed.append(f"{baseURL}{url}")
                print(f"Error: crawl({baseURL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
            else:
                print(f"Accepted:{baseURL}{url}")
                accepted.append(f"{baseURL}{url}")
                file = discectHTML(response.text)
                __buildJson(file, jsonFile)
                input("Input \"E\" to Continue")
        except Exception as e:
            print(f"Error: {baseURL}{url} is not accessible because {e}", file=sys.stderr)
        count += 1

    file = open("temp.txt", mode="w")
    print(json.dumps(jsonFile, indent=2),file=file)