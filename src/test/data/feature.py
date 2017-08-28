'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.feature import Feature
from data.variant import Variant


class TestFeature(unittest.TestCase):

    def testInit(self):
        feature = Feature()
        
        self.assertIsNone(feature.name)
        # Leerer Array ohne Preisdetails
        self.assertIsNotNone(feature.values)
        assert len(feature.values) == 0

        self.assertIsNone(feature.variants)
        self.assertIsNone(feature.unit)
        self.assertIsNone(feature.description)
        self.assertIsNone(feature.valueDetails)


        feature.unit = "mm"
        self.assertEqual(feature.unit, "mm")
        feature.description = "TestDescription"
        self.assertEqual(feature.description, "TestDescription")
        feature.valueDetails = "Details"
        self.assertEqual(feature.valueDetails, "Details")

    def testAddValue(self):
        # Single Value
        feature = Feature()
        feature.name = "Name"
        self.assertEqual( len(feature.values), 0)
        feature.addValue("Value")
        self.assertEqual( len(feature.values), 1)

    def testAddVariant(self):
        # Single Feature, Single ValueVariant
        feature = Feature()
        feature.name = "Name"
        variant = Variant()
        variant.productIdSuffix= "1L"
        variant.value = "Value" 
        feature.addVariantOrder(1)
        self.assertEqual(feature.variants.order, 1)
        self.assertEqual(len(feature.variants), 0)
        feature.addVariant(variant)
        self.assertEqual(len(feature.variants), 1)
    
    def testValidateExceptionFeatureNameMissing(self):
        feature = Feature()
        with self.assertRaisesRegex(Exception, "Der Merkmalsname fehlt."):
            feature.validate(True)

    def testValidateExceptionNoValueOrVariants(self):
        feature = Feature()
        feature.name = "TestFeature"
        with self.assertRaisesRegex(Exception, "Es wurden weder Attributswerte noch Varianten angegeben."):
            feature.validate(True)

        feature.values = None
        with self.assertRaisesRegex(Exception, "Es wurden weder Attributswerte noch Varianten angegeben."):
            feature.validate(True)

        feature.variants = None
        with self.assertRaisesRegex(Exception, "Es wurden weder Attributswerte noch Varianten angegeben."):
            feature.validate(True)

        feature.values = []
        with self.assertRaisesRegex(Exception, "Es wurden weder Attributswerte noch Varianten angegeben."):
            feature.validate(True)

    def testValidateExceptionValuesAndVariants(self):
        feature = Feature()
        feature.name = "TestFeature"
        feature.addValue("10")
        variant = Variant()
        variant.productIdSuffix = "01"
        variant.value = "Blau"
        feature.addVariant(variant)
        variant = Variant()
        variant.productIdSuffix = "02"
        variant.value = "Grün"
        feature.addVariant(variant)
        feature.addVariantOrder(1)
        
        with self.assertRaisesRegex(Exception, "Es wurden Values und Varianten angegeben. Die Zuordnung ist mehrdeutig."):
            feature.validate(True)


    def testValidateValue(self):
        feature = Feature()
        feature.name = "TestFeature"
        feature.addValue("10")
        feature.validate(True)

    def testValidateVariant(self):
        feature = Feature()
        feature.name = "TestFeature"
        variant = Variant()
        variant.productIdSuffix = "01"
        variant.value = "Blau"
        feature.addVariant(variant)
        variant = Variant()
        variant.productIdSuffix = "02"
        variant.value = "Grün"
        feature.addVariant(variant)
        feature.addVariantOrder(1)
        feature.validate(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    