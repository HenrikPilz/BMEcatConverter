'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import Variant


class VariantTest(unittest.TestCase):

    def testInit(self):
        variant = Variant()
        self.assertIsNone(variant.value)
        self.assertIsNone(variant.productIdSuffix)

    def testValidateExceptionVariantNotDefined(self):
        variant = Variant()
        with self.assertRaisesRegex(Exception, "Die Variante wurde nicht definiert."):
            variant.validate(True)

    def testValidateExceptionSuffixForVariantNotDefined(self):
        variant = Variant()
        variant.value = "10"
        with self.assertRaisesRegex(Exception, "Das Suffix fuer die Variante " + variant.value + " wurde nicht definiert."):
            variant.validate(True)

    def testValidate(self):
        variant = Variant()
        variant.value = "10"
        variant.productIdSuffix = "IT"
        variant.validate(True)

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
