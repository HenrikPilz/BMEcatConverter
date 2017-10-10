'''
Created on 09.10.2017

@author: Henrik Pilz
'''
import unittest
from importHandler.xml import BMEcatHandler as BMEcatImporter
from exportHandler.xml import BMEcatHandler as BMEcatExporter


class xmlHandlerTest(unittest.TestCase):


    def testName(self):
        bmecatHandler = BMEcatExporter()        
        bmecatHandler.writeBMEcatAsXML("test_bmecat.xml", [])
        
        #bmcatImporter = BMEcatImporter(dateFormat, decimalSeparator, thousandSeparator)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()