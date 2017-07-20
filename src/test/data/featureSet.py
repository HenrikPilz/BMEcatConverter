'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.feature import Feature
from data.featureSet import FeatureSet


class TestFeatureSet(unittest.TestCase):

    def testInit(self):
        featureSet = FeatureSet()
        # Default: kein Referenzsystem
        assert featureSet.referenceSytem is None
        # keine Referenzgruppen ID
        assert featureSet.referenceGroupId is None
        # Leerer Array ohne Features
        assert featureSet.features is not None
        assert len(featureSet.features) == 0

    def testAddFeature(self):
        # Single Feature, Single Value per Feature
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        assert len(featureSet) == 0
        featureSet.addFeature(feature)                
        assert len(featureSet) == 1        

    def testAddFeatureFailure(self):
        # Single Feature, Single Value per Feature
        featureSet = FeatureSet()
        feature = Feature()
        feature.addValue("Value")
        assert len(featureSet) == 0
        featureSet.addFeature(feature)                
        assert len(featureSet) == 0        

        feature = Feature()
        feature.name = "Name"
        assert len(featureSet) == 0
        featureSet.addFeature(feature)                
        assert len(featureSet) == 0        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    