'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import Feature, FeatureSet


class FeatureSetTest(unittest.TestCase):

    def testInit(self):
        featureSet = FeatureSet()
        # Default: kein Referenzsystem
        self.assertIsNone(featureSet.referenceSytem)
        # keine Referenzgruppen ID
        self.assertIsNone(featureSet.referenceGroupId)
        # Leerer Array ohne Features
        self.assertIsNotNone(featureSet.features)
        self.assertEqual(len(featureSet.features), 0)
        
    def testValidate(self):
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet.addFeature(feature)                
        featureSet.validate(True)
        featureSet.referenceGroupId = "01239"
        featureSet.validate(True)

    def testValidateEmpty(self):
        featureSet = FeatureSet()
        with self.assertRaisesRegex(Exception, "Keine Attribute fuer diese Attributgruppe vorhanden!"):
            featureSet.validate(True)

        featureSet.features = None
        with self.assertRaisesRegex(Exception, "Keine Attribute fuer diese Attributgruppe vorhanden!"):
            featureSet.validate(True)

    def testValidateExceptionReferenceGroupIdAndName(self):
        featureSet = FeatureSet()
        featureSet.referenceGroupId = "01239"
        featureSet.referenceGroupName = "TestGroupname"
        with self.assertRaisesRegex(Exception, "Es darf nur entweder eine Referenzgruppen ID oder ein Referenzgruppenname angegeben werden."):
            featureSet.validate(True)

    def testAddFeature(self):
        # Single Feature, Single Value per Feature
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        self.assertEqual(len(featureSet), 0)
        featureSet.addFeature(feature)                
        self.assertEqual(len(featureSet), 1)        

    def testAddFeatureFailure(self):
        # Single Feature, Single Value per Feature
        featureSet = FeatureSet()
        feature = Feature()
        feature.addValue("Value")
        self.assertEqual(len(featureSet), 0)
        featureSet.addFeature(feature)                
        self.assertEqual(len(featureSet), 0)       

        feature = Feature()
        feature.name = "Name"
        self.assertEqual(len(featureSet), 0)
        featureSet.addFeature(feature)                
        self.assertEqual(len(featureSet), 0)       

    def testEqualityOfEmptyAndEqualFeatureSets(self):
        featureSet1 = FeatureSet()
        self.assertNotEqual(featureSet1, None, "FeatureSet not equal to None")
        self.assertNotEqual(featureSet1, "", "FeatureSet not equal to str")
        featureSet2 = FeatureSet()
        
        self.assertEqual(featureSet1, featureSet2, "Two Empty FeatureSets should be equal.")
        self.assertTrue(featureSet1 == featureSet2, "Empty FeatureSets should be equal to another another via '=='")
        self.assertFalse(featureSet1 != featureSet2, "Empty FeatureSets should not be unequal to another another via '!='")

        featureSet1 = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet1.addFeature(feature)
        featureSet2 = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet2.addFeature(feature)
        
        self.assertEqual(featureSet1, featureSet2, "Two NonEmpty FeatureSets should be equal, if they contain the same Features")
        self.assertTrue(featureSet1 == featureSet2, "NonEmpty FeatureSets should be equal to another another via '==', if they contain the same Features")
        self.assertFalse(featureSet1 != featureSet2, "NonEmpty FeatureSets should not be unequal to another another via '!=', if they contain the same Features")

    def testEqualityOfDifferentFeatures(self):
        featureSet1 = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet1.addFeature(feature)
        featureSet2 = FeatureSet()
        
        self.assertNotEqual(featureSet1, featureSet2, "One nonempty FeatureSet and an empty FeatureSet should not be equal.")
        self.assertFalse(featureSet1 == featureSet2, "Empty FeatureSets should be equal to another another via '=='")
        self.assertTrue(featureSet1 != featureSet2, "Empty FeatureSets should not be unequal to another another via '!='")

    def testEqualityOfDifferentFeatureSets(self):
        featureSet1 = FeatureSet()
        featureSet2 = FeatureSet()
        
        self.assertEqual(featureSet1, featureSet2, "Two Empty FeatureSets should be equal.")
        self.assertTrue(featureSet1 == featureSet2, "Empty FeatureSets should be equal to another another via '=='")
        self.assertFalse(featureSet1 != featureSet2, "Empty FeatureSets should not be unequal to another another via '!='")

        featureSet1 = FeatureSet()
        feature = Feature()
        feature.name = "Name1"
        feature.addValue("Value1")
        featureSet1.addFeature(feature)
        featureSet2 = FeatureSet()
        feature = Feature()
        feature.name = "Name2"
        feature.addValue("Value2")
        featureSet2.addFeature(feature)
        
        self.assertNotEqual(featureSet1, featureSet2, "Two NonEmpty FeatureSets should not be equal, due to different Features")
        self.assertFalse(featureSet1 == featureSet2, "NonEmpty FeatureSets should not be equal to another another via '==', due to different Features")
        self.assertTrue(featureSet1 != featureSet2, "NonEmpty FeatureSets should be unequal to another another via '!=', due to different Features")

#if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
