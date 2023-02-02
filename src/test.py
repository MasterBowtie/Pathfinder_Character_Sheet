import unittest
from Tests import TestCharacterSheet, TestSkill

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCharacterSheet.TestCharacterSheet))
suite.addTest(unittest.makeSuite(TestSkill.TestSkill))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)