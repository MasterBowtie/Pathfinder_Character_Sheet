import unittest
import requests
from tools.getHTML import ImportHTML

URL = "https://2e.aonprd.com/"

class TestAncestries(unittest.TestCase):
    def test_ImportAncestry(self):
        jsonFile = {}
        testFiles = ["tools/Dwarf_test.json", "tools/Human_test.json", "tools/Shoony_test.json", \
                     "tools/Kobold_test.json", "tools/Android_test.json", "tools/Kitsune_test.json", \
                     "tools/Anadi_test.json"]
        testURL = []
        testURL.append("Ancestries.aspx?ID=1")
        testURL.append("Ancestries.aspx?ID=6")
        testURL.append("Ancestries.aspx?ID=16")
        testURL.append("Ancestries.aspx?ID=18")
        testURL.append("Ancestries.aspx?ID=27")
        testURL.append("Ancestries.aspx?ID=38")
        testURL.append("Ancestries.aspx?ID=42")
        index = 0
        while index < len(testFiles):
            character = ImportHTML().runDebug(testURL[index], jsonFile)
            tempfile = open("temp.txt", mode="w")
            print(character, file=tempfile)
            tempfile.close()
            tempfile = open("temp.txt", mode="r")
            character = tempfile.read()
            tempfile.close()
            file = open(f"{testFiles[index]}")
            text = file.read()
            file.close()
            self.assertEqual(character, text)
            index += 1

