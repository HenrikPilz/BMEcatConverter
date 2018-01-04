'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from lxml import etree

from datamodel import Variant
from datamodel import VariantSet


class VariantSetTest(unittest.TestCase):

    def testInit(self):
        variantSet = VariantSet()

        self.assertIsNone(variantSet.order)
        self.assertIsNotNone(variantSet.variants)
        self.assertEqual(len(variantSet.variants), 0)
        # testLen #1
        self.assertEqual(len(variantSet), 0)

    def testAddVariant(self):
        variantSet = VariantSet()
        variantSet.order = 1

        # testLen #1
        self.assertEqual(len(variantSet), 0)
        variant = Variant()
        variant.productIdSuffix = "1d"
        variant.value = "1"
        variantSet.addVariant(variant)
        # testLen #2
        self.assertEqual(len(variantSet.variants), 1)
        variant = Variant()
        variant.productIdSuffix = "1d"
        variant.value = "1"
        variantSet.addVariant(variant)
        self.assertEqual(len(variantSet), 1)

    def testValidateExceptionNoOrder(self):
        variantSet = VariantSet()
        with self.assertRaisesRegex(Exception, "Die Reihenfolge der Suffixe ist nicht definitiert."):
            variantSet.validate(True)

    def testValidateExceptionNoVariant(self):
        variantSet = VariantSet()
        variantSet.order = 1
        with self.assertRaisesRegex(Exception, "Keine Varianten fuer diesen Artikel vorhanden!"):
            variantSet.validate(True)

    def testValidate(self):
        variantSet = VariantSet()
        variantSet.order = 1
        variant = Variant()
        variant.value = 1
        variant.productIdSuffix = "IT"
        variantSet.addVariant(variant)
        variantSet.validate(True)

    def testEqual(self):
        variantSet1 = VariantSet()
        self.assertNotEqual(variantSet1, None, "VariantSet not equal to None")
        self.assertNotEqual(variantSet1, "", "VariantSet not equal to str")

        variantSet2 = VariantSet()

        self.assertEqual(variantSet1, variantSet2, "Empty VariantSets should be equal")
        self.assertTrue(variantSet1 == variantSet2, "Empty VariantSets should be equal via '==")
        self.assertFalse(variantSet1 != variantSet2, "Empty VariantSets should not be nonequal via '!='")

        variantSet1.order = 1
        variant = Variant()
        variant.value = 1
        variant.productIdSuffix = "IT"
        variantSet1.addVariant(variant)

        variantSet2.order = 2
        variant = Variant()
        variant.value = 1
        variant.productIdSuffix = "IT"
        variantSet2.addVariant(variant)

        self.assertEqual(variantSet1, variantSet2, "Empty VariantSets should be equal")
        self.assertTrue(variantSet1 == variantSet2, "Empty VariantSets should be equal via '==")
        self.assertFalse(variantSet1 != variantSet2, "Empty VariantSets should not be nonequal via '!='")

    def testToXML(self):
        variantSet = VariantSet()
        variantSet.order = 1
        variant = Variant()
        variant.value = "10"
        variant.productIdSuffix = "IT"
        variantSet.addVariant(variant)
        self.assertEqual(etree.tostring(variantSet.toXml()),
                         b'<VARIANTS><VORDER>1</VORDER><VARIANT><FVALUE>10</FVALUE><SUPPLIER_AID_SUPPLEMENT>IT</SUPPLIER_AID_SUPPLEMENT></VARIANT></VARIANTS>',
                         "XML Output Kaputt")

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
