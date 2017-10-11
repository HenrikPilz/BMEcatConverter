'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data import Feature, Variant


class FeatureTest(unittest.TestCase):

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

    def testEqualityOfEmptyFeatures(self):
        feature1 = Feature()
        feature2 = Feature()
        
        self.assertEqual(feature1, feature2, "Two Empty Features should be equal.")
        self.assertTrue(feature1 == feature2, "Empty Feature should be equal to another another via '=='")
        self.assertFalse(feature1 != feature2, "Empty Feature should not be unequal to another another via '!='")

    def testEqualityForDiferentTypesAndNone(self):
        feature1 = Feature()
        self.assertFalse(feature1 == None, "Empty Features should not be equal to None")
        self.assertTrue(feature1 != None, "Empty Features should be unequal to None")
 
        self.assertFalse(feature1 == "test", "Empty Features should not be equal to str('test')")
        self.assertTrue(feature1 != "test", "Empty Features should be unequal to str('test')")

    def testEqualityForDiferentValues(self):
        feature1 = Feature()
        feature1.name = "Test"
        feature1.addValue("1")
        feature1.unit = "TU"
        
        feature2 = Feature()
        feature2.name = "Test"
        feature2.addValue("1")
        feature2.unit = "TU"
        
        self.assertEqual(feature1, feature2, "Two Empty Features should be equal.")
        self.assertTrue(feature1 == feature2, "Empty Feature should be equal to another another via '=='")
        self.assertFalse(feature1 != feature2, "Empty Feature should not be unequal to another another via '!='")

        feature2.addValue("2")

        self.assertNotEqual(feature1, feature2, "Two Features should not be equal, because of different values.")
        self.assertFalse(feature1 == feature2, "Empty Feature should not be equal to another another via '==', because of different values")
        self.assertTrue(feature1 != feature2, "Empty Feature should be unequal to another another via '!=', because of different values")

        feature1.addValue("2")
        feature2.name = "Test2"

        self.assertNotEqual(feature1, feature2, "Two Features should not be equal, because of different names.")
        self.assertFalse(feature1 == feature2, "Empty Feature should not be equal to another another via '==', because of different names")
        self.assertTrue(feature1 != feature2, "Empty Feature should be unequal to another another via '!=', because of different names")

        feature2.unit = "CU"
        feature2.name = "Test"

        self.assertNotEqual(feature1, feature2, "Two Features should not be equal, because of different units.")
        self.assertFalse(feature1 == feature2, "Empty Feature should not be equal to another another via '==', because of different units")
        self.assertTrue(feature1 != feature2, "Empty Feature should be unequal to another another via '!=', because of different units")

        feature2.unit = "TU"
        feature2.description = "Testdescription"

        self.assertNotEqual(feature1, feature2, "Two Features should not be equal, because of different descriptions.")
        self.assertFalse(feature1 == feature2, "Empty Feature should not be equal to another another via '==', because of different descriptions")
        self.assertTrue(feature1 != feature2, "Empty Feature should be unequal to another another via '!=', because of different descriptions")


        feature2.addValue("2")

        self.assertNotEqual(feature1, feature2, "Two Features should not be equal, because of different values.")
        self.assertFalse(feature1 == feature2, "Empty Feature should not be equal to another another via '==', because of different values")
        self.assertTrue(feature1 != feature2, "Empty Feature should be unequal to another another via '!=', because of different values")

        
