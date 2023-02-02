import requests
import json

API_KEY = ""
URL = "https://api.pathfinder2.fr/v1/pf2"
HEADERS = {'Authorization': API_KEY}

def startInfoDump():
    file = open("Pathfinder_API.txt")
    global API_KEY
    API_KEY = file.read()
    global HEADERS
    HEADERS['Authorization'] = API_KEY

def fetchAncestries():
    print("starting")
    try:
        r = requests.get(f"{URL}/ancestry", headers=HEADERS)
        print("Connecting")
        for item in r.json()["results"]:
            newItem = json.dumps(item)
            name = item['name']
            fileString = f"ancestries/ancestries_{name}.txt"
            newFile = open(fileString, mode="w")
            print(newItem.replace('\u2011',""),file=newFile,end="")
    finally:
        print("Cannot Connect")
        getAncestries()


def getAncestries():

    '''
    r = requests.get(f"{URL}/ancestry", headers=HEADERS).json()
    count = r["count"]
    results = r["results"]
    ancestryList = {}
    name = ""
    for item in results:
        name = item['name']
        ancestryList[name] = {}
        for item2 in item['system']:
            #print(type(item2), item2, item['system'][item2])
            ancestryList[name][item2] = item['system'][item2]
        string = f"{name}\n\n"
        string += str(item['system']['description']['value'])\
            .replace('<li>', '\t- ').replace('</li>', '')\
            .replace('<p>', "").replace('</p>', "")\
            .replace('<em>', "").replace('</em>', "")\
            .replace('<hr />','')\
            .replace('<h2>', '\n\t').replace('</h2>', "") \
            .replace('<h3>', '\n\t').replace('</h3>', "") \
            .replace('<ul>', "").replace("</ul>", "")\
            .replace('\u2011', "")

        fileString = f"ancestries/ancestries_{name}.txt"
        ancestry = open(file=fileString, mode='w')
        print(string, file=ancestry, end="")
        ancestry = open(file=fileString, mode='r')
        string = ""
        for line in ancestry:
            if not line.startswith('<'):
                string += line
        ancestry = open(file=fileString, mode='w')
        print(string, file=ancestry, end="")
        print(string, end="")
        ancestry.close()
    return r
    '''

if __name__ == "__main__":
    startInfoDump()
    fetchAncestries()