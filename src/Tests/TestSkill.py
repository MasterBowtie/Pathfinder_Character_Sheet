import unittest

from data.skill import Skill

class TestSkill(unittest.TestCase):
    def test_SkillStats(self):
        skill = Skill("TestSkill", "Str", 1, 10)
        self.assertEqual(skill.getSkill(), "TestSkill")
        self.assertEqual(skill.getScore(), "Str")
        self.assertEqual(skill.getBonus(), 0)
        self.assertEqual(skill.getProficiency(), "Untrained")
        self.assertEqual(skill.getScoreValue(), 10)
        self.assertEqual(skill.getItem(), 0)
        self.assertFalse(skill.getArmor())
        self.assertFalse(skill.getArmorEq())
        self.assertEqual(skill.getArmorBonus(), 0)
        self.assertIsNone(skill.getDescription())
        with self.assertRaises(NameError):
            Skill("TestSkill", "Rel", 1, 10)
        with self.assertRaises(NameError):
            Skill("TestSkill", "Str", 1, 10, proficiency="Not Trained")

    def test_EditSkill(self):
        skill = Skill("TestSkill", "Str", 1, 10, True, "Trained")
        proficiencyList = ["Untrained", "Trained", "Expert", "Master", "Legendary"]
        bonusList = [0, 3, 5, 7, 9]
        skill.setSkill("SkillTest")
        self.assertEqual(skill.getSkill(), "SkillTest")

        count = 0
        for i in proficiencyList:
            skill.setProficiency(i)
            self.assertEqual(skill.getProficiency(), i)
            self.assertEqual(skill.getBonus(), bonusList[count])
            count += 1

        bonus = 9
        for i in range(1, 21):
            skill.setLevel(i)
            self.assertEqual(skill.getBonus(), bonus)
            bonus += 1

        for i in range (1, 21):
            skill.setArmorBonus(i)
            self.assertEqual(skill.getBonus(), bonus)
            bonus += 1
        bonus -= 6

        for i in range(1, 10, 2):
            skill.setScoreValue(i)
            self.assertEqual(skill.getBonus(), bonus)
            bonus += 1

        self.assertTrue(skill.getArmorEq())
        skill.equipArmor()
        self.assertFalse(skill.getArmorEq())
        self.assertEqual(skill.getBonus(), bonus - 21)

        skill.setDescription("Here are some words")
        self.assertEqual(skill.getDescription(), "Here are some words")



