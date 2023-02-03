import requests
import json

<<<<<<< HEAD

def editDescription(name, description):
    tempfile1 = open("temp.txt", mode="w")
    print(f"{name}\n {description}", file=tempfile1)
    tempfile1.close()
    tempfile2 = open("temp.txt", mode="r")
    newText = ""
    for line in tempfile2.readlines():
        write = True
        for char in line:
            if char == "<":
                write = False
            if write:
                newText += char
            if char == ">":
                write = True
    description = newText
    tempfile2.close()
    return description


# This make an API call for Ancestries
=======
def editDescription(description):
    print(description)
    input("Press Enter to Continue")
    return description
    pass

>>>>>>> main
def fetchAncestries(relPath):
    print("Fetching Ancestries...")
    try:
        URL = "https://api.pathfinder2.fr/v1/pf2"
        file = open(f"{relPath}Pathfinder_API.txt")
        API_KEY = file.read()
        file.close()
        HEADERS = {'Authorization': API_KEY}
        r = requests.get(f"{URL}/ancestry", headers=HEADERS)
        print("Connecting")
<<<<<<< HEAD
=======
        for item in r.json()["results"]:
            name = item['name']
            description = item["system"]["description"]["value"]
            item["system"]["description"]["value"] = editDescription(description)
            newItem = json.dumps(item,indent=3)\
                .replace('true', 'True').replace('false','False')
            fileString = f"{relPath}ancestries/ancestries_{name}.txt"
            newFile = open(fileString, mode="w")
            #print(newItem.find('\u2011'), name)
            print(newItem.replace('\u2011',""),file=newFile,end="")
            newFile.close()

    except:
        print("Cannot Connect")
    finally:
        getAncestries(relPath)

def fetchAncestryFeatures(relPath):
    print("Fetching Ancestry Features ...")
    try:
        URL = "https://api.pathfinder2.fr/v1/pf2"
        file = open(f"{relPath}Pathfinder_API.txt")
>>>>>>> main

        # This loads all the results into local json format
        ancestryList = {}
        for item in r.json()["results"]:
<<<<<<< HEAD
            # send it over to clean up and remove HTML junk
=======
            newItem = json.dumps(item,indent=3)\
                .replace('true', 'True').replace('false','False')
>>>>>>> main
            name = item['name']
            item["system"]["description"] = editDescription(name,
                                                            item["system"]["description"]["value"].replace('\u2011',
                                                                                                           ""))
            ancestryList[name] = item
        file = open(f"{relPath}ancestries.py", "w")

        # This saves all the local jsons into a single referable file
        string = "ANCENTRIES = {"
        for item in ancestryList:
            temp = json.dumps(ancestryList[item], indent=3).replace('true', 'True').replace('false', 'False')
            string += f"\"{item}\": {temp},\n"
        string += "}"
        print(string, file=file)
        file.close()

    except:
        print("Cannot Connect")
<<<<<<< HEAD

=======
    finally:
        getAncestryFeature(relPath)


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

    file = open(f"{relPath}ancestries.py", "w")
    string = "ANCENTRIES = {"
    for item in ancestryList:
        temp = json.dumps(ancestryList[item],indent=3)
        string += f"\"{item}\": {temp},\n"
    string += "}"
    print(string, file=file)
>>>>>>> main


if __name__ == "__main__":
    fetchAncestries("")
