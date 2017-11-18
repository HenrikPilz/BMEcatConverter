'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import Variant, VariantSet


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

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
