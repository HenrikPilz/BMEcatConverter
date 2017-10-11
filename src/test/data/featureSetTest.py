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

