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
        
        assert feature.name == None
        # Leerer Array ohne Preisdetails
        assert feature.values is not None
        assert len(feature.values) == 0

        assert feature.variants == None
        assert feature.unit == None
        assert feature.description == None
        assert feature.valueDetails == None


        feature.unit = "mm"
        assert feature.unit == "mm"
        feature.description = "TestDescription"
        assert feature.description == "TestDescription"
        feature.valueDetails = "Details"
        assert feature.valueDetails == "Details"

    def testAddValue(self):
        # Single Value
        feature = Feature()
        feature.name = "Name"
        assert len(feature.values) == 0
        feature.addValue("Value")
        assert len(feature.values) == 1        

    def testAddVariant(self):
        # Single Feature, Single ValueVariant
        feature = Feature()
        feature.name = "Name"
        variant = Variant()
        variant.productIdSuffix= "1L"
        variant.value = "Value" 
        feature.addVariantOrder(1)
        assert feature.variants.order == 1
        assert len(feature.variants) == 0
        feature.addVariant(variant)
        assert len(feature.variants) == 1

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    