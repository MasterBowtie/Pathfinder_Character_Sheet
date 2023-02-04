import requests
import json

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

        # This loads all the results into local json format
        ancestryList = {}
        for item in r.json()["results"]:
            # send it over to clean up and remove HTML junk
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



if __name__ == "__main__":
    fetchAncestries("")
