import json
import sys
import time

import requests

URL = "https://2e.aonprd.com/"

class ImportHTML():
    def buildAncestryJson(self,array, charJson):
        name = array[4]
        if "Heritage" in name:
            raise ImportError
        charJson[name] = {}
        self.setUpJson(charJson[name])

        description = ""
        extras = []
        index = 5
        resume = True


        while resume:
            #print(f"{index} {array[index]}")
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
        charJson[name]["extras"] = self.parseExtras(extras)
        #file = open(f"{name}.json", mode="w")
        #print(f"{json.dumps(charJson[name], indent=2)}", file=file)
        #file.close()
        return json.dumps(charJson[name], indent=2)

    # \u2013 == -
    # \u2011 == -
    # \u2014 == -
    # \u2019 == '
    def discectHTML(self, html):
        html = html.replace("\u2013", "-").replace("\u2011", "-").replace("\u2014", "-").replace("\u2019", "'")
        file = html.split("\n")
        write = False
        file2 = []

        # filter lines...
        for line in file:
            if write and "</div>" in line:
                write = False
            if "" != line.strip() and write:
                file2.append(line.strip())
            if "id=\"main\"" in line:
                write = True

        string = ""
        for line in file2:
            #print(line)
            line = line.replace("<span", "\n<span").replace("</span>", "\n</span>\n").replace("<li>", "\n\t- ")\
                .replace("<tr>", "\n<tr>").replace("</td><td>","|").replace("<br", "\n<br")\
                .replace("</h3>", "<split>\n").replace("</h2>", "<split>\n").replace("</h1>", "<split>\n") \
                .replace("<hr", "\n<split>Body:<").replace("<h", "\n<split>Heading:<").replace("&nbsp;", "")
            string += line
        file = string.split("<split>")

        file2 = ""
        for line in file:
            file2 += line
        file = file2.split("\n")

        file2 = ""
        for line in file:
            #print(line)
            file2 += f"{line}\n"
            if line.startswith("<span alt="):
                items = self.parseAltText(line)
                file2 += f"\ntrait: {items['alt'].split(' ')[0]}\n"
                file2 += f"\nalt: {items['title']}\n"
        file = file2.split("\n")

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
        file.append("eof")

        count = 0
        found = False
        while count < len(file):
            if len(file[count].strip()) == 0:
                file.pop(count)
            else:
                #print(f"{count} {file[count]}")
                count += 1
        return file

    def parseAltText(self, line):
        items = {}
        write = False
        item = ""
        key = ""
        for char in line:
            if char == "=":
                key = item
                item = ""
            if char == "\"":
                write = not write
            if not write and char == " ":
                if key != "" and item != "<span":
                    items[key.strip()] = item.removesuffix('><a').strip("\"")
                item = ""
            if char != "=":
                item += char
        return items

    def parseExtras(self, extras):
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
                        ability, index = self.buildAbility(extras[index:], index)
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

    def buildAbility(self, abilities, prev):
        abilityDict = {}
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
                if abilities[index].startswith("Heading"):
                    break
                if abilities[index].startswith("Body:"):
                    abilityDict[ability]["description"] += abilities[index].split(":")[1]
                index += 1
        return abilityDict, index + prev



    def setUpJson(self, param):
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

    def runMain(self, count, target, jsonFile):
        while count < target:
            url = f"Ancestries.aspx?ID={count}"
            try:
                response = requests.get(f"{URL}{url}")
                if not response.ok:
                    print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
                else:
                    print(f"Accepted:{URL}{url}")
                    file = self.discectHTML(response.text)
                    self.buildAncestryJson(file, jsonFile)
            except Exception as e:
                print(f"Error: {URL}{url} is not accessible because {e}", file=sys.stderr)
            count += 1

    def runDebug(self,url, jsonFile):
        try:
            response = requests.get(f"{URL}{url}")
            if not response.ok:
                print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
            else:
                print(f"Accepted:{URL}{url}")
                file = self.discectHTML(response.text)
                character = self.buildAncestryJson(file, jsonFile)
                return character
        except Exception as e:
            print(f"Error: {URL}{url} is not accessible because {e}", file=sys.stderr)
            return ""


    # Tests
    # https://2e.aonprd.com/Ancestries.aspx?ID=15
    # https://2e.aonprd.com/Ancestries.aspx?ID=18
    # https://2e.aonprd.com/Ancestries.aspx?ID=27
    # https://2e.aonprd.com/Ancestries.aspx?ID=38
    # https://2e.aonprd.com/Ancestries.aspx?ID=42
    # https://2e.aonprd.com/Ancestries.aspx?ID=48
    # https://2e.aonprd.com/Ancestries.aspx?ID=49
    # https://2e.aonprd.com/Ancestries.aspx?ID=53
    # https://2e.aonprd.com/Ancestries.aspx?ID=56

def main():
    debug = False
    jsonFile = {}

    if debug:
        testList = []
        # testList.append("Ancestries.aspx?ID=1")
        # testList.append("Ancestries.aspx?ID=6")
        # testList.append("Ancestries.aspx?ID=16")
        # testList.append("Ancestries.aspx?ID=18")
        # testList.append("Ancestries.aspx?ID=27")
        # testList.append("Ancestries.aspx?ID=38")
        # testList.append("Ancestries.aspx?ID=42")
        # testList.append("Ancestries.aspx?ID=48")
        # testList.append("Ancestries.aspx?ID=49")
        # testList.append("Ancestries.aspx?ID=53")
        # testList.append("Ancestries.aspx?ID=56") #Resolved?
        index = 0
        for url in testList:
            character = ImportHTML().runDebug(url, jsonFile)
            print(character)

    else:
        ImportHTML().runMain(1, 60, jsonFile)
        time.sleep(5)
        print(f"\nTotal Ancestries: {len(jsonFile)}")
        for character in jsonFile:
            print(character)
        file = open("../reference/ancestries.py", mode="w")
        print(f"ANCESTRIES = {json.dumps(jsonFile, indent=1)}", file=file)
        file.close()

if __name__ == "__main__":
    main()