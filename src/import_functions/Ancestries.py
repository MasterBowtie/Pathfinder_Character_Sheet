import requests
import json
import os

def fetchAncestries(relPath):
    print("starting")
    try:
        URL = "https://api.pathfinder2.fr/v1/pf2"
        file = open(f"{relPath}Pathfinder_API.txt")

        API_KEY = file.read()
        file.close()
        HEADERS = {'Authorization': API_KEY}
        r = requests.get(f"{URL}/ancestry", headers=HEADERS)
        print("Connecting")
        for item in r.json()["results"]:
            newItem = json.dumps(item)
            name = item['name']
            fileString = f"{relPath}ancestries/ancestries_{name}.txt"
            newFile = open(fileString, mode="w")
            #print(newItem.find('\u2011'), name)
            print(newItem.replace('\u2011',""),file=newFile,end="")
            newFile.close()

    except:
        print("Cannot Connect")
    finally:
        getAncestries(relPath)


def getAncestries(relPath):
    directory = os.listdir(f"{relPath}ancestries")
    ancestryList = {}

    for file in directory:
        try:
            file = open(f"{relPath}ancestries/{file}")
            result = json.loads(file.read())
            ancestryList[result['name']] = result
            file.close()
            #print(ancestryList[result['name']])
        except:
            print(f"Error: Cannot read {file}")

    file = open(f"{relPath}ancestries_constants.py", "w")
    string = "ANCENTRIES = {"
    for item in ancestryList:
        temp = json.dumps(ancestryList[item],indent=3)\
            .replace('true', 'True').replace('false','False') \
            .replace("<li>", "\t- ").replace("</li>", "") \
            .replace("<p>", "").replace("</p>", "") \
            .replace("<em>", "").replace("</em>", "").replace("<hr />", "") \
            .replace("<h2>", "\\n\\t").replace("</h2>", "") \
            .replace("<h3>", "\\n\\t").replace("</h3>", "") \
            .replace("<ul>", "").replace("</ul>", "")\
            .replace("<strong>", "").replace("</strong>",": ")


        string += f"\"{item}\": {temp},\n"
    string += "}"
    print(string, file=file)

if __name__ == "__main__":
    fetchAncestries("")