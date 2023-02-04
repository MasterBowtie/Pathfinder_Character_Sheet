import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin




def setUPJSON(param):
    param["source"] = ""
    param["trait"] = {}
    param["languages"] = []
    param["addLanguages"] = []
    param["boosts"] = []
    param["flaws"] = []


if __name__ == "__main__":
    baseURL = "https://2e.aonprd.com/"
    url = "Ancestries.aspx?ID=1"
    response = requests.get(f"{baseURL}{url}")
    html = response.text
    html.replace('\ue50e', "")
    file = open("temp.txt", mode="w")
    print(html, file=file)
    file.close()

    file = open("temp.txt")
    file2 = open("temp2.txt", mode="w")
    newText = ""
    line = file.readline().strip()
    count = 0
    write = False

    while "</html>" not in line:
        if "id=\"main\"" in line:
            write = True
        if write and "</div>" in line:
            write = False
        if "\n" != line and write:
            newText += line
            count += 1
        line = file.readline()

    newText += "\neof\n"
    print(newText.replace("<", "\n").replace(">", "\n"), file=file2)
    file.close()
    file2.close()

    file = open("temp2.txt")
    file2 = open("temp.txt", mode="w")
    newText = ""
    line = file.readline().strip()
    while "eof" not in line:
        if len(line.strip()) == 0 or line.startswith("/") or line.startswith("h2") or line.startswith("br")\
                or line.startswith("img") or line.startswith(","):
            line = file.readline()
            continue
        else:
            newText += line
            line = file.readline()
    newText += "\neof\n"
    print(newText, file=file2)
    file.close()
    file2.close()

    dict = {}
    name = ""
    found = False

    newText = ""
    file2 = open("temp.txt")
    count = 0
    line = file2.readline()
    while "eof" not in line:
        if url in line and not found:
            line = file2.readline()
            if line.strip() != "u":
                name = line.strip()
                dict[name] = {}
                file2.seek(0)
                found = True
                setUPJSON(dict[name])
            line = file2.readline()

        if "Source" == line.strip():
            line = file2.readline()
            while line.strip() != "i":
                line = file2.readline()
                if line.strip() == "i":
                    nextLine = file2.readline()
                    dict[name]["source"] = nextLine.strip()

                    break

            line = "Description\n"

        if "class=\"trait\"" in line and found:
            list1 = line.split("\"")
            dict[name]["trait"][list1[1]] = list1[5]
            line = file2.readline()

        if "Hit Points" == line.strip():
            line = file2.readline().strip()
            dict[name]["hp"] = line
            line = file2.readline()

        if "Size" == line.strip():
            line = file2.readline().strip()
            dict[name]["size"] = line
            line = file2.readline()

        if "Speed" == line.strip():
            line = file2.readline().strip()
            dict[name]["speed"] = line
            line = file2.readline()

        if "Ability Boosts" == line.strip():
            line = file2.readline()
            while line.strip() != "Ability Flaw(s)":
                dict[name]["boosts"].append(line.strip())
                line = file2.readline()

        if "Ability Flaw(s)" == line.strip():
            line = file2.readline()
            while line.strip() != "Languages":
                dict[name]["flaws"].append(line.strip())
                line = file2.readline()

        if "Languages" == line.strip():
            line = file2.readline().strip()
            while "a href=\"Languages.aspx?ID=" in line:
                line = file2.readline()
                dict[name]["languages"].append(line.strip())
                line = file2.readline().strip()

        if "Additional languages" in line:
            line = file2.readline()
            while "Languages.aspx?ID=" in line:
                line = file2.readline()
                dict[name]["addLanguages"].append(line.strip())
                line = file2.readline()

        newText += f"{line}"
        count += 1
        line = file2.readline()
    file2.close()
    if "Darkvision" in newText:
        dict[name]["vision"] = "Darkvision"
    elif "Low-Light Vision" in newText:
        dict[name]["vision"] = "Low-Light Vision"
    else:
        dict[name]["vision"] = "Normal"
    newText += "\neof\n"

    print(newText)
    file = open(f"{name}.json", mode="w")
    string = json.dumps(dict)
    print(json.dumps(dict, indent=2), file=file)
    file.close()



    '''
        
        
    '''
