'''
Created on 19.11.2017

@author: Henrik Pilz
'''
import os
import unittest

from mapping import UnitMapper


class UnitsTest(unittest.TestCase):

    def testUnitMapperWithoutFile(self):
        unitMapper = UnitMapper(None)
        unitMapper.readFile()

    def testUnitMapperWithTestFile(self):
        baseDirectory = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data", "units.csv")
        unitMapper = UnitMapper(baseDirectory)
        self.assertEqual(unitMapper.getSIUnit("test"), "", "Eintrag 'test' nicht in Einheitenliste.")
        self.assertEqual(unitMapper.getSIUnit("Bla"), "BLA", "Eintrag 'Bla' nicht in Einheitenliste.")


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
