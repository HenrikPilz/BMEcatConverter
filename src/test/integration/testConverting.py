'''
Created on 28.11.2017

@author: henrik.pilz
'''
import os
import unittest

from converter import DateFormatMissingException
from transformer.separators import NumberFormatException
import main


class TestMainConverter(unittest.TestCase):

    def testExcelToXmlWrongSeparators(self):
        testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data")
        inputFilePath = os.path.join(testDataPath, "TestPriceIsNumberAndTaxIsString.xlsx")

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xlsx', 'xml')]
        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
            main.main(args)

        args = ['--separators=english', '-i', inputFilePath, '-o', inputFilePath.replace('xlsx', 'xml')]
        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
            main.main(args)

        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('xlsx', 'xml')]
        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
            main.main(args)

        args = ['-i', 'Test.xlsx', '-o', 'test.xml']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 5)

    def testCreateBMEcatFullDataWrongSeparators(self):
        testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data")
        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullDataSeparatorsWrong.xml")

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xml', 'xlsx')]
        with self.assertRaisesRegex(DateFormatMissingException, "Zum Konvertieren von XML in Excel muss ein Datumsformat angegeben werden."):
            main.main(args)

        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullDataSeparatorsWrong.xml")

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xml', 'xlsx')]
        with self.assertRaisesRegex(DateFormatMissingException, "Zum Konvertieren von XML in Excel muss ein Datumsformat angegeben werden."):
            main.main(args)

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xml', 'xlsx'), '--dateformat="%Y-%m-%d"']
        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
            main.main(args)

        args = ['-i', 'Test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 5)

    def testCreateBMEcatFullData(self):
        testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data")
        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullData.xml")

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xml', 'xlsx'), '--dateformat="%Y-%m-%d"']
        main.main(args)

    def testCreateExcelFullData(self):
        testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data")
        inputFilePath = os.path.join(testDataPath, "testCreateExcelFullData.xlsx")

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xlsx', 'xml'), '--dateformat="%Y-%m-%d"']
        main.main(args)

    def testHelp(self):
        main.main(['-h'])

    def testConversionModeExceptionThrown(self):
        testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data")
        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullData.xlsm")

        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('xlsm', 'xml')]
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 2)

        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullData.png")
        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('png', 'xml')]
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 2)

        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullData.xlsx")
        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('xlsx', 'png')]
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 2)

    def testRelativePathButFail(self):
        testDataPath = os.path.join("..", "..", "test_data")
        inputFilePath = os.path.join(testDataPath, "testCreateBMEcatFullDataSeparatorsWrong.xml")

        args = ['-i', inputFilePath, '-o', inputFilePath.replace('xml', 'xlsx'), '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 5)

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
