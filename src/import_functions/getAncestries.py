import requests
from bs4 import BeautifulSoup
import brotli #required for request decryption
from urllib.parse import urlparse, urljoin

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
# def fetchAncestries(relPath):
    # print("Fetching Ancestries...")
    # try:
    #     URL = "https://api.pathfinder2.fr/v1/pf2"
    #     file = open(f"{relPath}Pathfinder_API.txt")
    #     API_KEY = file.read()
    #     file.close()
    #     HEADERS = {'Authorization': API_KEY}
    #     r = requests.get(f"{URL}/ancestry", headers=HEADERS)
    #     print("Connecting")

    #     # This loads all the results into local json format
    #     ancestryList = {}
    #     for item in r.json()["results"]:
    #         # send it over to clean up and remove HTML junk
    #         name = item['name']
    #         item["system"]["description"] = editDescription(name,
    #                                                         item["system"]["description"]["value"].replace('\u2011',
    #                                                                                                        ""))
    #         ancestryList[name] = item
    #     file = open(f"{relPath}ancestries.py", "w")

    #     # This saves all the local jsons into a single referable file
    #     string = "ANCENTRIES = {"
    #     for item in ancestryList:
    #         temp = json.dumps(ancestryList[item], indent=3).replace('true', 'True').replace('false', 'False')
    #         string += f"\"{item}\": {temp},\n"
    #     string += "}"
    #     print(string, file=file)
    #     file.close()

    # except:
    #     print("Cannot Connect")
URL = "https://2e.aonprd.com"
TARGET = "Ancestries.aspx"

def fetchAncestries():
    print("Fetching Ancestries...")
    
    response = requests.get(f"{URL}/{TARGET}")
    if not response.ok:
        print("A problem was encountered")

    html = BeautifulSoup(response.text, "html.parser")
    links = html.find_all("a")
    ancestryIDs = getAncestryLinks(links)

    for i in range(1,3):
        response = requests.get(f"{URL}/{TARGET}?{ancestryIDs[i]}")
        if not response.ok:
            print("A problem was encountered")
        parseAncestryHTML(f"{TARGET}?{ancestryIDs[i]}", BeautifulSoup(response.text, "html.parser"))

            

def getAncestryLinks(links):
    ancestryIDs = []
    for a in links:
        link = a.get("href")
        if isinstance(link, str) and link.startswith(TARGET):
            ids = link.split("?")
            if (len(ids) == 2 and ids[1].startswith("ID") and ids[1] not in ancestryIDs):
                ancestryIDs.append(ids[1])
    return ancestryIDs

def parseAncestryHTML(url, html):
    query = {
        "A_name": "",
        "A_size": "",
        "traits": "",
        "health": 0,
        "speed": 0,
        "A_description": "",
        "languages": "",
        "senses": "",
        "source": ""
    }
    score = {
        "strength": 0,
        "dexterity": 0,
        "constitution": 0,
        "intelligence": 0,
        "wisdom": 0,
        "charisma": 0,
        "free": 0
    }

    file = open("textFile","w")
    print(html, file=file)
    file.close()

    links = html.find_all("a")
    for a in links:
        link = a.get("href")
    
    # Get the Name
        if link == url and not "Details" in a.get_text():
            query["A_name"] = a.get_text()
    # Get the Source
        if "class" in a.attrs and a["class"][0] == "external-link":
            query["source"] = a.get_text()


    # Get the traits
    traitsClass = html.find_all(class_="trait")
    traits = []
    for trait in traitsClass:
        traits.append(trait.get_text())
    query["traits"] = ",".join(traits)

    print(json.dumps(query, indent=2))


if __name__ == "__main__":
    fetchAncestries()

