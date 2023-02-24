import unittest
from Tests import TestCharacterSheet, TestSkill, TestAncestries

suite = unittest.TestSuite()
#suite.addTest(unittest.makeSuite(TestCharacterSheet.TestCharacterSheet))
#suite.addTest(unittest.makeSuite(TestSkill.TestSkill))
suite.addTest(unittest.makeSuite(TestAncestries.TestAncestries))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)