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
        outputFilePath = os.path.join(self.outputPath, "testPriceIsNumberAndTaxIsString.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

        args = ['--separators=english', '-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

        args = ['--separators=german', '-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

        args = ['-i', 'Test.xlsx', '-o', 'test.xml']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 5)

    def testConvertExcelToXmlWrongSeparatorsInDeliveryTime(self):
        inputFilePath = os.path.join(self.testDataPath, "testConvertExcelToXmlWrongSeparatorsInDeliveryTime.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testConvertExcelToXmlWrongSeparatorsInDeliveryTime.xml")

        args = ['--separators=english', '-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

    def testConvertBMEcatMissingOptions(self):
        inputFilePath = os.path.join(self.testDataPath, "testConvertBMEcatMissingOptions.xml")
        outputFilePath = os.path.join(self.outputPath, "testConvertBMEcatMissingOptions.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

        args = ['-i', 'Test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 5)

    def testConvertExcelNonExistent(self):
        inputFilePath = os.path.join(self.testDataPath, "testConvertExcelNonExistent.xlsm")
        outputFilePath = os.path.join(self.outputPath, "testConvertExcelNonExistent.xml")

        args = ['--separators=german', '-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 5)

    def testConversionModeExceptionThrown(self):
        inputFilePath = os.path.join(self.testDataPath, "testConversionModeExceptionThrown.png")
        outputFilePath = os.path.join(self.outputPath, "testConversionModeExceptionThrown.xml")
        args = ['--separators=german', '-i', inputFilePath, '-o', outputFilePath]
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 2)

        inputFilePath = os.path.join(self.testDataPath, "testConversionModeExceptionThrown.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testConversionModeExceptionThrown.png")
        args = ['--separators=german', '-i', inputFilePath, '-o', outputFilePath]

        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 2)

    def testRelativePathButFail(self):
        inputFilePath = os.path.join("../test_data", "testRelativePathButFail.xml")
        outputFilePath = os.path.join(self.outputPath, "testRelativePathButFail.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 5)

    def testMissingArgumentException(self):
        outputFilePath = os.path.join(self.outputPath, "testMissingArgumentException.xml")

        args = ['-i', '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 3)

    def testGetoptOptErrorException(self):
        outputFilePath = os.path.join(self.outputPath, "testMissingArgumentException.xml")

        args = ['-p', '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 3)

    def testCreateExcelFullDataDTDNotFoundException(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFullDataWithCategoryTreeAndDTDNotExistent.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFullDataWithCategoryTreeAndDTDNotExistent.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 5)

    def testCreateExcelNestedArticleDetailsException(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelNestedArticleDetailsException.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelNestedArticleDetailsException.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

    def testCreateExcelArticleDetailsOutOfArticleException(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelArticleDetailsOutOfArticleException.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelArticleDetailsOutOfArticleException.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

    def testCreateBMEcatNoPossibleSheet(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatNoPossibleSheet.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatNoPossibleSheet.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

    def testCreateBMEcatTwoPossibleSheets(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatTwoPossibleSheets.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatTwoPossibleSheets.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

    def testConvertExcelToBMEcatExceptionFormulaFound(self):
        inputFilePath = os.path.join(self.testDataPath, "testConvertExcelToBMEcatExceptionFormulaFound.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testConvertExcelToBMEcatExceptionFormulaFound.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runAndAssertSystemExitAndNotOutputfile(args, outputFilePath, 6)

    def __runAndAssertSystemExitAndNotOutputfile(self, args, outputFilePath, exitcode):
        with self.assertRaises(SystemExit) as cm:
            main.main(args)
        self.assertEqual(cm.exception.code, exitcode)
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
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelFromBMEcatFullDataFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFromBMEcatFullDataFiege.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFromBMEcatFullDataFiege.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelFromBMEcatFullDataDoubleEntries(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFromBMEcatFullDataDoubleEntries.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFromBMEcatFullDataDoubleEntries.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateBMEcatFromExcelFullDataNonFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFromExcelFullDataNonFiege.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatFromExcelFullDataNonFiege.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"', '--merchant=contorion']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateBMEcatFromExcelFullDataFiege(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFromExcelFullDataFiege.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatFromExcelFullDataFiege.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateBMEcatFromExcelFullDataGTINAlsZahl(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateBMEcatFromExcelFullDataGTINAlsZahl.xlsx")
        outputFilePath = os.path.join(self.outputPath, "testCreateBMEcatFromExcelFullDataGTINAlsZahl.xml")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelFullDataWithCategoryTreeAndDTD(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFullDataWithCategoryTreeAndDTD.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFullDataWithCategoryTreeAndDTD.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelFullDataWithReferenceWithoutType(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelFullDataWithReferenceWithoutType.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelFullDataWithReferenceWithoutType.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelUserDefinedExtensionHaveFeatures(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelUserDefinedExtensionHaveFeatures.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelUserDefinedExtensionHaveFeatures.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testDateWithoutType(self):
        inputFilePath = os.path.join(self.testDataPath, "testDateWithoutType.xml")
        outputFilePath = os.path.join(self.outputPath, "testDateWithoutType.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat="%Y-%m-%d"']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelWithPriceValidity(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelWithPriceValidity.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelWithPriceValidity.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat=%Y-%m-%d']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelWithDateWithNotUsedType(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelWithDateWithNotUsedType.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelWithDateWithNotUsedType.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat=%Y-%m-%d']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def testCreateExcelWithoutProductId(self):
        inputFilePath = os.path.join(self.testDataPath, "testCreateExcelWithoutProductId.xml")
        outputFilePath = os.path.join(self.outputPath, "testCreateExcelWithoutProductId.xlsx")

        args = ['-i', inputFilePath, '-o', outputFilePath, '--dateformat=%Y-%m-%d']
        self.__runTestAssertOutputFileExists(args, outputFilePath)

    def __runTestAssertOutputFileExists(self, args, outputFilePath):
        main.main(args)

        self.assertTrue(os.path.exists(outputFilePath))


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
