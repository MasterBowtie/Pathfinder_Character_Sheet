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
TARGET = "Ancestries.aspx"
MY_DB = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database="Pathfinder"
)

# Connect to the offical Pathfinder Source
def fetchAncestries():
    print("Fetching Ancestries...")
    
    response = requests.get(f"{URL}/{TARGET}")
    if not response.ok:
        print("A problem was encountered")

    html = BeautifulSoup(response.text, "html.parser")
    links = html.find_all("a")
    ancestryIDs = getAncestryLinks(links)

    for i in range(len(ancestryIDs)):
        response = requests.get(f"{URL}/{TARGET}?{ancestryIDs[i]}")
        if not response.ok:
            print("A problem was encountered")
        html = BeautifulSoup(response.text, "html.parser")
        main = html.find(class_="main")
        ancestry, scores = parseAncestryHTML(f"{TARGET}?{ancestryIDs[i]}", main)
        insertToDatabase(ancestry, scores)

#This gets all the links for the Ancestries
def getAncestryLinks(links):
    ancestryIDs = []
    for a in links:
        link = a.get("href")
        if isinstance(link, str) and link.startswith(TARGET):
            ids = link.split("?")
            if (len(ids) == 2 and ids[1].startswith("ID") and ids[1] not in ancestryIDs):
                ancestryIDs.append(ids[1])
    return ancestryIDs

# This parses the data from the url and turns it into two objects
def parseAncestryHTML(url, html):
    query = {
        "A_name": "",
        "A_size": "",
        "traits": "",
        "health": 0,
        "speed": 0,
        "A_description": "",
        "languages": "",
        "abilities": "",
        "source": ""
    }
    scores = {
        "strength": 0,
        "dexterity": 0,
        "constitution": 0,
        "intelligence": 0,
        "wisdom": 0,
        "charisma": 0,
        "free": 0
    }

    #Adding sentries
    addDescription = False
    addBoost = False
    addFlaw = False
    addLanguages = False
    addAbilities = False


    DescriptionBuilder = []
    strings = []
    languages = []
    abilities = []

    for string in html.stripped_strings:
        strings.append(repr(string).strip("'"))

    for i in range(len(strings)):
        #Build the Description
        if "pg." in strings[i] :
            addDescription = True
            continue
        if "Mechanics" in strings[i]:
            addDescription = False
        if addDescription:
            DescriptionBuilder.append(strings[i])
        
        #Get Single Items
        if strings[i] == "Hit Points":
            query["health"] = int(strings[i+1])
        if strings[i] == "Size":
            query["A_size"] = strings[i+1]
        if strings[i] == "Speed":
            query["speed"] = strings[i+1]
        
        #Get Boosts and Flaws
        if "Ability Boost" in strings[i]:
            addBoost = True
        if "Ability Flaw" in strings[i]:
            addBoost = False
            addFlaw = True
        if strings[i] == "Two free ability boosts":
            scores["free"] = 2
        if addBoost and strings[i].lower() in scores:
            scores[strings[i].lower()] += 1
        if addFlaw and strings[i].lower() in scores:
            scores[strings[i].lower()] -= 1

        #Deactivate Abilites and watch for languages and Senses
        if strings[i] == "Languages":
            addBoost = False
            addFlaw = False
            addLanguages = True
            continue
        if "Additional" in strings[i]:
            addLanguages = False
        if "prevalent" in strings[i]:
            addAbilities = True
            continue
        if addLanguages and strings[i] != ",":
            languages.append(strings[i])
        if addAbilities:
            abilities.append(strings[i])
    
    query["A_description"] = "\n".join(DescriptionBuilder)
    query["languages"] = ",".join(languages)
    query["abilities"] = "\n".join(abilities)
    # print(query["abilities"])

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

    return query, scores

def insertToDatabase(ancestries, scores):
    mycursor = MY_DB.cursor()

    sql = "SELECT * FROM ancestries WHERE A_name = %s"
    mycursor.execute(sql, [ancestries["A_name"]])

    # If no referece found, add to the Database
    if len(mycursor.fetchall()) == 0:
        #build string for scores insert
        sql = "INSERT INTO scores (" + ", ".join(list(scores.keys())) + ") VALUES (" + "%s, "*(len(scores.keys()) - 1) + "%s)"
        #build tuple for scores insert
        val = tuple([scores[value] for value in list(scores.keys())])
        mycursor.execute(sql,val)

        ancestries["scoreID"] = mycursor.lastrowid

        sql = "INSERT INTO ancestries (" + ", ".join(list(ancestries.keys())) + ") VALUES (" + "%s, "*(len(ancestries.keys()) - 1) + "%s)"
        val = val = tuple([ancestries[value] for value in list(ancestries.keys())])
        try:
            mycursor.execute(sql,val)
        except Exception as e:
            print("Oops!")
            print(json.dumps(ancestries, indent=2))

        MY_DB.commit()
        print(ancestries["A_name"], "record inserted.")

    #If name found, update the ancestry instead.
    else:

        sql = "UPDATE ancestries (" + ", ".join(list(ancestries.keys())) + ") VALUES (" + "%s, "*(len(ancestries.keys()) - 1) + "%s) WHERE A_name = %s"
        val = list(ancestries.keys())
        val.append(ancestries["A_name"])
        print(ancestries["A_name"], "record updated.")

if __name__ == "__main__":
    fetchAncestries()

