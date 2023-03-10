import json
import sys
import time
import requests
from import_functions.import_Ancestries import buildAncestryJson, importHeritage, buildVersatile

URL = "https://2e.aonprd.com/"

class ImportHTML():


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
        index = 0
        for line in file:

            if write and line.strip() == "</div>":
                write = False
            if write:
                file2.append(line.strip())
                #print(f"{index} {line}")
            if "id=\"main\"" in line:
                write = True
            index += 1

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
            if "class=\"trait\"" in line:
                file2 += f"trait:{line}\n"
            else:
                file2 += f"{line}\n"
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

    def importAncestries(self, jsonFile):
        count = 1
        target = 60 #approximate amount of Ancestries
        while count < target:
            url = f"Ancestries.aspx?ID={count}"
            try:
                response = requests.get(f"{URL}{url}")
                if not response.ok:
                    print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
                else:
                    print(f"Accepted:{URL}{url}")
                    file = self.discectHTML(response.text)
                    buildAncestryJson(file, jsonFile)
            except Exception as e:
                print(f"Error: {URL}{url} is not accessible because {e}", file=sys.stderr)
            count += 1
        count = 1
        target = 230 #approximate amount of  heritages
        while count < target:
            url = f"Heritages.aspx?ID={count}"
            try:
                response = requests.get(f"{URL}{url}")
                if not response.ok:
                    print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
                else:
                    print(f"Accepted:{URL}{url}")
                    file = self.discectHTML(response.text)
                    importHeritage(file, jsonFile)
            except Exception as e:
                print(f"Error: {URL}{url} is not accessible because {e}", file=sys.stderr)
            count += 1



    def debugAncestries(self,url, jsonFile):
        response = requests.get(f"{URL}{url}")
        if not response.ok:
            print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
        else:
            print(f"Accepted:{URL}{url}")
            file = self.discectHTML(response.text)
            character = buildAncestryJson(file, jsonFile)
            return character

    def debugHeritages(self, url, jsonFile):
        response = requests.get(f"{URL}{url}")
        if not response.ok:
            print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
        else:
            print(f"Accepted:{URL}{url}")
            file = self.discectHTML(response.text)
            importHeritage(file, jsonFile)

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
    debug = True
    heritage = True
    jsonFile = {}

    # TODO
    response = requests.get(f"{URL}Rules.aspx?ID=1417")
    if not response.ok:
        print(f"Error: crawl({URL}Rules.aspx?ID=1417) {response.status_code} {response.reason}", file=sys.stderr)
    else:
        print(f"Accepted:{URL}Rules.aspx?ID=1417")
        file = ImportHTML().discectHTML(response.text)
        buildVersatile(jsonFile, file)
    exit()

    if debug and heritage:
        testList = []
        testList.append("Ancestries.aspx?ID=1") #Dwarf
        #testList.append("Ancestries.aspx?ID=6") #Human
        #testList.append("Ancestries.aspx?ID=7") #Half-Elf
        #testList.append("Ancestries.aspx?ID=16") #Shoony
        #testList.append("Ancestries.aspx?ID=22") #Changling
        testList.append("Ancestries.aspx?ID=43") #Conrasu

        for url in testList:
            ImportHTML().debugAncestries(url, jsonFile)
        testList = []
        testList.append("Heritages.aspx?ID=1")  #Dwarf
        testList.append("Heritages.aspx?ID=2")  #Dwarf
        #testList.append("Heritages.aspx?ID=54") #Shoony
        #testList.append("Heritages.aspx?ID=82") #Changling
        testList.append("Heritages.aspx?ID=161")  #Conrasu

        for url in testList:
            ImportHTML().debugHeritages(url, jsonFile)
        print(json.dumps(jsonFile, indent=2))

    elif debug and not heritage:
        testList = []
        #testList.append("Ancestries.aspx?ID=1")
        #testList.append("Ancestries.aspx?ID=6")
        #testList.append("Ancestries.aspx?ID=16")
        #testList.append("Ancestries.aspx?ID=18") #Kobold
        #testList.append("Ancestries.aspx?ID=27")
        #testList.append("Ancestries.aspx?ID=38") #Kitsune
        #testList.append("Ancestries.aspx?ID=42")
        #testList.append("Ancestries.aspx?ID=48")
        #testList.append("Ancestries.aspx?ID=49")
        #testList.append("Ancestries.aspx?ID=53")
        #testList.append("Ancestries.aspx?ID=56") #Resolved?
        for url in testList:
            character = ImportHTML().debugAncestries(url, jsonFile)
            print(character)

    else:
        ImportHTML().importAncestries(jsonFile)
        time.sleep(5)
        print(f"\nTotal Ancestries: {len(jsonFile)}")
        for character in jsonFile:
            print(character)
        file = open("../constants/ancestries.py", mode="w")
        print(f"ANCESTRIES = {json.dumps(jsonFile, indent=1)}", file=file)
        file.close()

if __name__ == "__main__":
    main()
