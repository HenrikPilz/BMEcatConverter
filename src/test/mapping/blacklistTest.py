'''
Created on 19.11.2017

@author: Henrik Pilz
'''
import os
import unittest

from mapping import Blacklist


class BlacklistTest(unittest.TestCase):

    def testUnitMapperWithoutFile(self):
        blacklist = Blacklist(None)
        blacklist.readFile()

    def testUnitMapperWithTestFile(self):
        baseDirectory = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data", "blacklist.csv")
        blacklist = Blacklist(baseDirectory)
        self.assertTrue(blacklist.contains("test"), "Eintrag 'test' nicht in Blacklist.")
        self.assertTrue(blacklist.contains("Bla"), "Eintrag 'Bla' nicht in Blacklist.")
        self.assertTrue(blacklist.contains("BLA"), "Eintrag 'BLA' nicht in Blacklist.")


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
