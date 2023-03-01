import json
import sys
import time
import requests
from import_Ancestries import buildAncestryJson

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

    def importAncestries(self, count, target, jsonFile):
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

    def debugAncestries(self,url, jsonFile):
        response = requests.get(f"{URL}{url}")
        if not response.ok:
            print(f"Error: crawl({URL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
        else:
            print(f"Accepted:{URL}{url}")
            file = self.discectHTML(response.text)
            character = buildAncestryJson(file, jsonFile)
            return character

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

    if debug and heritage:
        testList = []
        testList.append("Ancestries.aspx?ID=7")
        for url in testList:
            character = ImportHTML().debugAncestries(url, jsonFile)
            print(character)

    elif debug and not heritage:
        testList = []
        testList.append("Ancestries.aspx?ID=1")
        testList.append("Ancestries.aspx?ID=6")
        testList.append("Ancestries.aspx?ID=16")
        testList.append("Ancestries.aspx?ID=18")
        testList.append("Ancestries.aspx?ID=27")
        testList.append("Ancestries.aspx?ID=38")
        testList.append("Ancestries.aspx?ID=42")
        testList.append("Ancestries.aspx?ID=48")
        testList.append("Ancestries.aspx?ID=49")
        testList.append("Ancestries.aspx?ID=53")
        testList.append("Ancestries.aspx?ID=56") #Resolved?
        for url in testList:
            character = ImportHTML().debugAncestries(url, jsonFile)
            #print(character)

    else:
        ImportHTML().importAncestries(1, 60, jsonFile)
        time.sleep(5)
        print(f"\nTotal Ancestries: {len(jsonFile)}")
        for character in jsonFile:
            print(character)
        file = open("../constants/ancestries.py", mode="w")
        print(f"ANCESTRIES = {json.dumps(jsonFile, indent=1)}", file=file)
        file.close()

if __name__ == "__main__":
    main()
