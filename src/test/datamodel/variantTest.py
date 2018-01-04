'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from lxml import etree

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
        with self.assertRaisesRegex(Exception, "Das Suffix fuer die Variante '{0}' wurde nicht definiert.".format(variant.value)):
            variant.validate(True)

    def testValidate(self):
        variant = Variant()
        variant.value = "10"
        variant.productIdSuffix = "IT"
        variant.validate(True)

    def testEqual(self):
        variant1 = Variant()
        self.assertNotEqual(variant1, None, "Variant not equal to None")
        self.assertNotEqual(variant1, "", "Variant not equal to str")

        variant2 = Variant()

        self.assertEqual(variant1, variant2, "Empty Variants should be equal")
        self.assertTrue(variant1 == variant2, "Empty Variants should be equal via '==")
        self.assertFalse(variant1 != variant2, "Empty Variants should not be nonequal via '!='")

    def testToXML(self):
        variant = Variant()
        variant.value = "10"
        variant.productIdSuffix = "IT"
        self.assertEqual(etree.tostring(variant.toXml()),
                         b'<VARIANT><FVALUE>10</FVALUE><SUPPLIER_AID_SUPPLEMENT>IT</SUPPLIER_AID_SUPPLEMENT></VARIANT>',
                         "XML Output Kaputt")

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
