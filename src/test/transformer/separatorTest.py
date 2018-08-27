'''
Created on 17.11.2017

@author: henrik.pilz
'''
import unittest

from error import NumberFormatException
from error import SeparatorNotDetectableException
from transformer import SeparatorTransformer


class SeparatorTransformerTest(unittest.TestCase):

    def testSeparatorAutoDetectExceptionAtThirdValueFirstNotDetectable(self):
        for firstInputValue, firstvalidationValue, secondInputValue, secondValidationValue, thirdInputValue, exceptionMessage in [
                                (180, 180, "180.", 180, "180,", "Thousandseparator ',' found in wrong position for value '180,'."),
                                (180, 180, "180,", 180, "180.", "Thousandseparator '.' found in wrong position for value '180.'."),
                                (180, 180, "180.01", 180.01, "180,01", "Thousandseparator '.' found in wrong position for value '180,01'."),
                                (180, 180, "180.01", 180.01, "180,12312,221", "Thousandseparator '.' found in wrong position for value '180,12312,221'."),
                                (180, 180, "180.01", 180.01, "180,00.01", "Thousandseparator ',' found in wrong position for value '180,00.01'."),
                                (180, 180, "180.01", 180.01, "18.00,01", "Decimalseparator '.' found in wrong position for value '18.00,01'."),
                                (180, 180, "180.01", 180.01, "19,180,00.01", "Thousandseparator ',' found in wrong position for value '19,180,00.01'."),
                                (180, 180, "180.01", 180.01, "19.018.00,01", "Decimalseparator '.' occurs more than once: '19.018.00,01'"),
                                (180, 180, "180.01", 180.01, "19.180,00.01", "Decimalseparator '.' found in wrong position for value '19.180,00.01'."),
                                (180, 180, "180.01", 180.01, "19,180.00.01", "Decimalseparator '.' occurs more than once: '19,180.00.01'")]:
            separatorTransformer = SeparatorTransformer()
            self.assertEqual(firstvalidationValue, separatorTransformer.transform(firstInputValue),
                             "1 Aus '{0} sollte {1} werden.".format(firstInputValue, firstvalidationValue))
            self.assertEqual(secondValidationValue, separatorTransformer.transform(secondInputValue),
                             "2 Aus '{0} sollte {1} werden.".format(firstInputValue, secondValidationValue))
            with self.assertRaisesRegex(NumberFormatException, exceptionMessage):
                separatorTransformer.transform(thirdInputValue)

    def testSeparatorAutoDetectExceptionAtSecondValue(self):
        for firstInputValue, validationValue, secondInputValue, exceptionMessage in [
                                ("180.", 180, "180,", "Thousandseparator ',' found in wrong position for value '180,'."),
                                ("180,", 180, "180.", "Thousandseparator '.' found in wrong position for value '180.'."),
                                ("180.01", 180.01, "180,12312,221", "Thousandseparator '.' found in wrong position for value '180,12312,221'."),
                                ("180.01", 180.01, "180,00.01", "Thousandseparator ',' found in wrong position for value '180,00.01'."),
                                ("180.01", 180.01, "18.00,01", "Decimalseparator '.' found in wrong position for value '18.00,01'."),
                                ("180.01", 180.01, "19,180,00.01", "Thousandseparator ',' found in wrong position for value '19,180,00.01'."),
                                ("180.01", 180.01, "19.018.00,01", "Decimalseparator '.' occurs more than once: '19.018.00,01'"),
                                ("180.01", 180.01, "19.180,00.01", "Decimalseparator '.' found in wrong position for value '19.180,00.01'."),
                                ("180.01", 180.01, "19,180.00.01", "Decimalseparator '.' occurs more than once: '19,180.00.01'")]:
            separatorTransformer = SeparatorTransformer()
            self.assertEqual(validationValue, separatorTransformer.transform(firstInputValue),
                             "Aus '{0} sollte {1} werden.".format(firstInputValue, validationValue))
            with self.assertRaisesRegex(NumberFormatException, exceptionMessage):
                separatorTransformer.transform(secondInputValue)

    def testSeparatorAutoDetectException(self):
        for inputValue, exceptionMessage in [
                                ("180.12312.221", "Could not detect Separators for value '180.12312.221'."),
                                ("180,12312,221", "Could not detect Separators for value '180,12312,221'."),
                                ("180,00.01", "Could not detect Separators."),
                                ("18.00,01", "Could not detect Separators."),
                                ("19,180,00.01", "Could not detect Separators."),
                                ("19.018.00,01", "Could not detect Separators."),
                                ("19.180,00.01", "Could not detect Separators."),
                                ("19,180.00.01", "Could not detect Separators."),
                                ("18,00.01", "Could not detect Separators.")]:
            self._transformRaiseException(inputValue, SeparatorNotDetectableException, exceptionMessage)

    def testSeparatorEnglishException(self):
        for inputValue, exceptionMessage in [ (" , ", "Thousandseparator ',' is set wrongly: ','"),
                                              (" 180, ", "Thousandseparator ',' found in wrong position."),
                                              ("180,0001", "Thousandseparator ',' found in wrong position."),
                                              ("18.000,01", "Decimalseparator '.' found in wrong position."),
                                              ("18.00,01", "Decimalseparator '.' found in wrong position for value '18.00,01'."),
                                              ("180,00.01", "Thousandseparator ',' found in wrong position for value '180,00.01'."),
                                              ("180.12312.221", "Decimalseparator '.' occurs more than once: '180.12312.221'"),
                                              ("180,12312,221", "Thousandseparator ',' found in wrong position for value '180,12312,221'."),
                                              ("1.918.000,01", "Decimalseparator '.' occurs more than once: '1.918.000,01'"),
                                              ("19,180,00.01", "Thousandseparator ',' found in wrong position for value '19,180,00.01'."),
                                              ("19.018.00,01", "Decimalseparator '.' occurs more than once: '19.018.00,01'"),
                                              ("19.180,00.01", "Decimalseparator '.' found in wrong position for value '19.180,00.01'."),
                                              ("19,180.00.01", "Decimalseparator '.' occurs more than once: '19,180.00.01'")
                                              ]:
            self._transformRaiseException(inputValue, NumberFormatException, exceptionMessage, "english")

    def testSeparatorGermanException(self):
        for inputValue, exceptionMessage in [ (" . ", "Thousandseparator '.' is set wrongly: '.'"),
                                              (" 180. ", "Thousandseparator '.' found in wrong position."),
                                              ("180.0001", "Thousandseparator '.' found in wrong position for value '180.0001'."),
                                              ("180,00.01", "Decimalseparator ',' found in wrong position for value '180,00.01'."),
                                              ("18,000.01", "Decimalseparator ',' found in wrong position for value '18,000.01'."),
                                              ("18.00,01", "Thousandseparator '.' found in wrong position for value '18.00,01'."),
                                              ("180.12312.221", "Thousandseparator '.' found in wrong position for value '180.12312.221'."),
                                              ("180,12312,221", "Decimalseparator ',' occurs more than once: '180,12312,221'"),
                                              ("1,918,000.01", "Decimalseparator ',' occurs more than once: '1,918,000.01'"),
                                              ("19,180.00.01", "Decimalseparator ',' found in wrong position for value '19,180.00.01'."),
                                              ("19.180,00.01", "Decimalseparator ',' found in wrong position for value '19.180,00.01'."),
                                              ("19.018.00,01", "Thousandseparator '.' found in wrong position for value '19.018.00,01'."),
                                              ("19,180,00.01", "Decimalseparator ',' occurs more than once: '19,180,00.01'")
                                              ]:
            self._transformRaiseException(inputValue, NumberFormatException, exceptionMessage, "german")

    def testSeparatorEnglishValid(self):
        for inputValue, validationValue in [
                                (None, None),
                                ("", None),
                                ("  ", None),
                                (180, 180),
                                ("180", 180), (" 180", 180), ("180 ", 180), (" 180 ", 180),
                                (" 180. ", 180.0),
                                ("180.0001", 180.0001),
                                ("18,000.01", 18000.01),
                                ("1,918,000.01", 1918000.01)]:
            self._transformEnglish(inputValue, validationValue)

    def testSeparatorGermanValid(self):
        for inputValue, validationValue in [
                                (None, None),
                                ("  ", None),
                                ("", None),
                                (180, 180),
                                ("180", 180), (" 180", 180), ("180 ", 180), (" 180 ", 180),
                                (" 180, ", 180.0),
                                ("180,0001", 180.0001),
                                ("18.000,01", 18000.01),
                                ("1.918.000,01", 1918000.01)]:
            self._transformGerman(inputValue, validationValue)

    def testSeparatorAutoDetectValid(self):
        for inputValue, validationValue in [
                                (None, None),
                                ("", None),
                                (180, 180),
                                ("180", 180), (" 180", 180), ("180 ", 180), (" 180 ", 180),
                                (" 180. ", 180.0), (" 180, ", 180.0),
                                ("180.01", 180.01), ("180,01", 180.01),
                                ("180.001", 180.001), ("180,001", 180.001),
                                ("180.0001", 180.0001), ("180,0001", 180.0001),
                                ("18,000.01", 18000.01), ("18.000,01", 18000.01),
                                ("1,918,000.01", 1918000.01), ("1.918.000,01", 1918000.01)]:
            self._transformAutoDetect(inputValue, validationValue)

    def _transformAutoDetect(self, inputValue, validationValue):
        self._transform(inputValue, validationValue)

    def _transformEnglish(self, inputValue, validationValue):
        self._transform(inputValue, validationValue, "english")

    def _transformGerman(self, inputValue, validationValue):
        self._transform(inputValue, validationValue, "german")

    def _transform(self, inputValue, validationValue, mode=None):
        separatorTransformer = SeparatorTransformer(mode)
        self.assertEqual(validationValue, separatorTransformer.transform(inputValue), "Aus '{0} sollte {1} werden.".format(inputValue, validationValue))

    def _transformRaiseException(self, inputValue, exceptionType, exceptionMessage, mode=None):
        separatorTransformer = SeparatorTransformer(mode)
        with self.assertRaisesRegex(exceptionType, exceptionMessage):
            separatorTransformer.transform(inputValue)


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
