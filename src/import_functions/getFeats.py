import requests
from bs4 import BeautifulSoup
import brotli #required for request decryption
from urllib.parse import urlparse, urljoin
import json
import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
URL = "https://2e.aonprd.com"
TARGET = "Feats.aspx"
MY_DB = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database="Pathfinder"
)

# Connect to the offical Pathfinder Source
def fetchFeats():
    print("Fetching Feats...")
    featsIDs = getFeatLinks()

    for i in range(len(featsIDs)):
        response = requests.get(f"{URL}/{TARGET}?{featsIDs[i]}")
        if not response.ok:
            print("A problem was encountered")
        html = BeautifulSoup(response.text, "html.parser")
        main = html.find(class_="main")
        feat = parseFeatHTML(f"{TARGET}?{featsIDs[i]}", main)
        insertToDatabase(feat)

def getFeatLinks():
    validIDs = []
    for i in range(2109,2110):
        response = requests.get(f"{URL}/{TARGET}")
        if not response.ok:
            print("A problem was encountered")
        else:
            featID = f"ID={i}"
            validIDs.append(featID)

    print(i)
    return validIDs

def parseFeatHTML(url, html):
    feat = {
        "F_name": "",
        "F_description": "",
        "traits": "",
        "source": "",
        "F_level": 0
    }

    links = html.find_all("a")
    for a in links:
        link = a.get("href")
    
        # Get the Name
        if link == url:
            feat["F_name"] = a.get_text()

    #Initialize Sentries
    gotLevel = False
    addTrait = False
    addDescription = False

    description = []
    traits = []

    strings = []
    for string in html.stripped_strings:
        strings.append(repr(string).strip("'").strip(" . "))

    i = 0
    while i < len(strings):
        
        if strings[i] == feat["F_name"] and not gotLevel:
            feat["F_level"] = int(strings[i+1].strip("Feat "))
            gotLevel = True
            # print(strings[i])
        if strings[i] == "Source":
            feat["source"] = strings[i+1]
            addDescription = True
            i += 2
        if strings[i].replace(".", "", 1).isdigit() and addDescription:
            i += 1
        if strings[i] == "Traits":
            addTrait = True
            addDescription = False
            i += 1
        if addDescription:
            description.append(strings[i])
        if addTrait:
            traits.append(strings[i])
        i += 1

    # file = open("testfile.txt", "w")
    # print("\n".join(strings), file=file)
    # file.close()

    feat["F_description"] = " ".join(description).strip()
    feat["traits"] = "\n".join(traits)
    print(json.dumps(feat, indent=2))
    pass

def insertToDatabase(feat):
    pass


if __name__ == "__main__":
    fetchFeats()