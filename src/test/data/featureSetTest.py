'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data import Feature, FeatureSet


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

    def testEqualityOfEmptyFeatureSets(self):
        featureSet1 = FeatureSet()
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

