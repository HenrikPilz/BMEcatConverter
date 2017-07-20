'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.feature import Feature
from data.featureSet import FeatureSet
from data.mime import Mime
from data.product import Product
from data.productDetails import ProductDetails
from data.reference import Reference
from data.variant import Variant


class TestVariant(unittest.TestCase):

    def testInit(self):
        variant = Variant()
        assert variant.value == None
        assert variant.productIdSuffix == None

    def testValidate(self):
        variant = Variant()
        try:
            variant.validate(True)
        except Exception as ve:
            assert str(ve) ==  "Die Variante wurde nicht definiert."

        variant.value = "10"
        try:
            variant.validate(True)
        except Exception as ve:
            assert str(ve) == "Das Suffix fuer die Variante " + self.value + " wurde nicht definiert."


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    