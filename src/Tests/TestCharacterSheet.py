import unittest

from data.characterData import CharacterData, SKILLSLIST

# TODO: Add more
class TestCharacterSheet(unittest.TestCase):
    def test_NewCharacter(self):
        character = CharacterData()
        self.assertEqual(character.getScore("Str"), 10)
        self.assertEqual(character.getScore("Dex"), 10)
        self.assertEqual(character.getScore("Con"), 10)
        self.assertEqual(character.getScore("Int"), 10)
        self.assertEqual(character.getScore("Wis"), 10)
        self.assertEqual(character.getScore("Cha"), 10)
        with self.assertRaises(NameError):
            character.getScore("Rel")

        for skill in SKILLSLIST:
            skill, isFound = character.searchSkills(skill[0])
            self.assertTrue(isFound)
        skill, isFound = character.searchSkills("None")
        self.assertIsNone(skill)
        self.assertFalse(isFound)

    def test_EditCharacter(self):
        character = CharacterData()
        scoreList = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
        for score in scoreList:
            for i in range(20):
                character.setScore(score, i)
                self.assertEqual(character.getScore(score), i)
