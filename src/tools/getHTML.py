import json
import sys
import requests

def buildJson(array):
    pass

def discectHTML(html):
    html = html.replace('\ue50e', "").replace('\u2011', "")
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
        line = line.replace("<span", "\n<span").replace("</span>", "\n</span>\n")
        line = line.replace("alt=", "\nalt=").replace("<b", "\n<b").replace("</b>", "</b>\n")
        line  = line.replace("</h3>", "</h3>\n").replace("</h2>", "</h2>\n").replace("</h1>", "</h>\n")
        string += line.replace("<h", "\n<h")
    file = string.split("\n")

    newText = ""
    for line in file:
        if "span" in line or "" == line or "div" in line:
           pass
        else:
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
    while True:
        if "alt=" in file[0]:
            file.pop(0)
            break
        file.pop(0)
    count = 0
    for line in file:
        print(f"{count} {line}")
        count += 1



def discectHTML1(html, url):
    html = html.replace('\ue50e', "").replace('\u2011', "")
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
        if len(line.strip()) == 0 or line.startswith("/") or line.startswith("h2") or line.startswith("br") \
                or line.startswith("img") or line.startswith(","):
            line = file.readline()
            continue
        else:
            newText += line
            line = file.readline()
    newText += "\neof\n"
    if "ID=6" in url:
        print(newText)
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
                __setUPJSON(dict[name])
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
            if line.strip() == "Two free ability boosts":
                dict[name]["boosts"].append("Free")
                dict[name]["boosts"].append("Free")
                line = file2.readline()
            else:
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

    #print(newText)
    file = open(f"{name}.json", mode="w")
    string = json.dumps(dict, indent=2)
    #print(string)
    print(string, file=file)
    file.close()

def __setUPJSON(param):
    param["source"] = ""
    param["trait"] = {}
    param["languages"] = []
    param["addLanguages"] = []
    param["boosts"] = []
    param["flaws"] = []
    param["vision"] = {}
    param["extras"] = {}


if __name__ == "__main__":
    baseURL = "https://2e.aonprd.com/"
    count = 1
    accepted = []
    failed = []
    while count < 11:
        url = f"Ancestries.aspx?ID={count}"
        try:
            response = requests.get(f"{baseURL}{url}")
            if not response.ok:
                failed.append(f"{baseURL}{url}")
                print(f"Error: crawl({baseURL}{url}) {response.status_code} {response.reason}", file=sys.stderr)
            else:
                print(f"Accepted:{baseURL}{url}")
                accepted.append(f"{baseURL}{url}")
                discectHTML(response.text)
        except Exception as e:
            print(f"Error: {baseURL}{url} is not accessible because {e}", file=sys.stderr)

        count += 1




    '''
        
        
    '''
