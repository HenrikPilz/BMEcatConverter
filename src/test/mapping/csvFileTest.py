'''
Created on 19.11.2017

@author: Henrik Pilz
'''
import os
import unittest

from mapping.csvfile import CsvFile


class CsvFileTest(unittest.TestCase):

    def testCsvFileWithoutFile(self):
        CsvFile(None)

    def testUnitMapperWithTestFile(self):
        baseDirectory = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data", "blacklist.csv")
        with self.assertRaises(NotImplementedError):
            CsvFile(baseDirectory)


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
