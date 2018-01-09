'''
Created on 28.11.2017

@author: henrik.pilz
'''
import os
import unittest

import main


class TestMainConverter(unittest.TestCase):

    testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_data")
    outputPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "test_output")

    def testConvertExcelToXmlWrongSeparators(self):
        inputFilePath = os.path.join(self.testDataPath, "testPriceIsNumberAndTaxIsString.xlsx")
        outputFilePath = inputFilePath.replace('xlsx', 'xml')

        args = ['-i', inputFilePath, '-o', outputFilePath]
#        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
        with self.assertRaises(SystemExit) as cm1:
            main.main(args)
        self.assertEqual(cm1.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

        args = ['--separators=english', '-i', inputFilePath, '-o', outputFilePath]
#        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
        with self.assertRaises(SystemExit) as cm2:
            main.main(args)
        self.assertEqual(cm2.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

        args = ['--separators=german', '-i', inputFilePath, '-o', outputFilePath]
#        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
        with self.assertRaises(SystemExit) as cm3:
            main.main(args)
        self.assertEqual(cm3.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

        args = ['-i', 'Test.xlsx', '-o', 'test.xml']
        with self.assertRaises(SystemExit) as cm4:
            main.main(args)
        self.assertEqual(cm4.exception.code, 5)

    def testConvertBMEcatMissingOptions(self):
        inputFilePath = os.path.join(self.testDataPath, "testConvertBMEcatMissingOptions.xml")
        outputFilePath = os.path.join(self.outputPath, "testConvertBMEcatMissingOptions.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath]
#        with self.assertRaisesRegex(DateFormatMissingException, "Zum Konvertieren von XML in Excel muss ein Datumsformat angegeben werden."):
        with self.assertRaises(SystemExit) as cm1:
            main.main(args)
        self.assertEqual(cm1.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
#        with self.assertRaisesRegex(NumberFormatException, "Das Format '[0-9]{1,3}.?[0-9]{0,2}' stimmmt nicht mit den gewählten Separatoren überein."):
        with self.assertRaises(SystemExit) as cm2:
            main.main(args)
        self.assertEqual(cm2.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

        args = ['-i', 'Test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm3:
            main.main(args)
        self.assertEqual(cm3.exception.code, 5)

        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFullData.xlsm")

        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('xlsm', 'xml')]
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 5)

    def testConversionModeExceptionThrown(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFullData.png")
        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('png', 'xml')]
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 2)

        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFullData.xlsx")
        args = ['--separators=german', '-i', inputFilePath, '-o', inputFilePath.replace('xlsx', 'png')]
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 2)

    def testRelativePathButFail(self):
        inputFilePath = os.path.join("../test_data", "testRelativePathButFail.xml")
        outputFilePath = os.path.join(self.outputPath, "testRelativePathButFail.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 5)
        self.assertFalse(os.path.exists(outputFilePath))

    def testMissingArgumentException(self):
        outputFilePath = os.path.join(self.outputPath, "testMissingArgumentException.xml")

        args = ['-i', '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 3)
        self.assertFalse(os.path.exists(outputFilePath))

    def testGetoptOptErrorException(self):
        outputFilePath = os.path.join(self.outputPath, "testMissingArgumentException.xml")

        args = ['-p', '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 3)
        self.assertFalse(os.path.exists(outputFilePath))

    def testCreateExcelFullDataDTDNotFoundException(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFullDataWithCategoryTreeAndDTDNotExistent.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFullDataWithCategoryTreeAndDTDNotExistent.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 5)
        self.assertFalse(os.path.exists(outputFilePath))

    def testCreateExcelNestedArticleDetailsException(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelNestedArticleDetailsException.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelNestedArticleDetailsException.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

    def testCreateExcelArticleDetailsOutOfArticleException(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelArticleDetailsOutOfArticleException.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelArticleDetailsOutOfArticleException.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, 6)
        self.assertFalse(os.path.exists(outputFilePath))

    '''
    -------------------------------------
    --- Ab hier funktioniert's :)
    -------------------------------------
    '''
    def testHelp(self):
        main.main(['-h'])

    '''
    -------------------------------------
    --- Ab hier richtige Konvertierungen
    -------------------------------------
    '''
    def testCreateExcelFromBMEcatFullDataNonFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFromBMEcatFullDataNonFiege.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFromBMEcatFullDataNonFiege.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"', '--merchant=contorion']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelFromBMEcatFullDataFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFromBMEcatFullDataFiege.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFromBMEcatFullDataFiege.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelFromBMEcatFullDataDoubleEntries(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFromBMEcatFullDataDoubleEntries.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFromBMEcatFullDataDoubleEntries.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateBMEcatFromExcelFullDataNonFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFromExcelFullDataNonFiege.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatFromExcelFullDataNonFiege.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"', '--merchant=contorion']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateBMEcatFromExcelFullDataFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFromExcelFullDataFiege.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatFromExcelFullDataFiege.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateBMEcatFromExcelFullDataGTINAlsZahl(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFromExcelFullDataGTINAlsZahl.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatFromExcelFullDataGTINAlsZahl.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelFullDataWithCategoryTreeAndDTD(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFullDataWithCategoryTreeAndDTD.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFullDataWithCategoryTreeAndDTD.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelFullDataWithReferenceWithoutType(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFullDataWithReferenceWithoutType.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFullDataWithReferenceWithoutType.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelUserDefinedExtensionHaveFeatures(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelUserDefinedExtensionHaveFeatures.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelUserDefinedExtensionHaveFeatures.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testDateWithoutType(self):
        inputFilePath = os.path.join(self.testDataPath, "testDateWithoutType.xml")
        outputFilePath = os.path.join(self.outputPath, "testDateWithoutType.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelWithPriceValidity(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelWithPriceValidity.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelWithPriceValidity.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat=%Y-%m-%d']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelWithDateWithNotUsedType(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelWithDateWithNotUsedType.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelWithDateWithNotUsedType.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat=%Y-%m-%d']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))

    def testCreateExcelWithoutProductId(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelWithoutProductId.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelWithoutProductId.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat=%Y-%m-%d']
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
