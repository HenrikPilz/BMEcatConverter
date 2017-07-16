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


class TestProduct(unittest.TestCase):

    def testInit(self):
        product = Product()
        # Default: keine ProductID
        assert product.productId is None
        # keine Details
        assert product.details is None
        # keine OrderDetails
        assert product.orderDetails is None
        # Leerer Array ohne Preisdetails
        assert product.priceDetails is not None
        assert len(product.priceDetails) == 0
        # Leerer Array ohne Bilder
        assert product.mimeInfo is not None
        assert len(product.mimeInfo) == 0
        # Leerer Array ohne Attribute
        assert product.featureSets is not None
        assert len(product.featureSets) == 0
        # Leerer Array ohne Referenzen
        assert product.references is not None
        assert len(product.references) == 0
        # Leerer Array ohne Varianten
        assert product.variants is not None
        assert len(product.variants) == 0
        # Leerer Array ohne UserDefinedExtensions
        assert product.userDefinedExtensions is not None
        assert len(product.userDefinedExtensions.keys()) == 0
        # Keine Varianten gegeben
        assert product.hasVariants == False
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        assert product.numberOfVariants == 1

    def testDetails(self):
        product = Product()
        
        # setzen der Product ID       
        product.productId = "12345"
        assert product.productId == "12345"
        # Productdetails
        product.details = ProductDetails()
        
        product.addTitle("TestTitel")
        assert product.details.title == "TestTitel"
        
        product.addDescription("TestBeschreibung")
        assert product.details.description == "TestBeschreibung"

        product.addManufacturerId("12345")
        assert product.details.manufacturerId == "12345"

        product.addManufacturerName("Test")
        assert product.details.manufacturerName == "Test"

        product.addEAN("1234567890123")
        assert product.details.ean == "1234567890123"

        product.addDeliveryTime(2)
        assert product.details.deliveryTime == 2

        assert len(product.details.keywords) == 0
        product.addKeyword("TestKeyword")
        assert len(product.details.keywords) == 1
        assert "TestKeyword" in product.details.keywords

        assert len(product.details.specialTreatmentClasses) == 0
        product.addSpecialTreatmentClass("TestClass")
        assert len(product.details.specialTreatmentClasses) == 1
        assert "TestClass" in product.details.specialTreatmentClasses

    def testAddMime(self):
        product = Product()
        assert len(product.mimeInfo) == 0
        product.addMime(Mime())
        assert len(product.mimeInfo) == 1        
            
    def testAddReference(self):
        product = Product()
        assert len(product.references) == 0
        product.addReference(Reference())
        assert len(product.references) == 1        

    def testAddUserDefinedExtension(self):
        product = Product()
        assert len(product.userDefinedExtensions) == 0
        product.addUserDefinedExtension("")
        assert len(product.userDefinedExtensions) == 0
        # Aktuell passiert hier noch nichts        

    def testAddFeatureSetSingleValueFeature(self):
        # Single Feature, Single Value per Feature
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet.addFeature(feature)                
        assert len(product.featureSets) == 0
        product.addFeatureSet(featureSet)
        assert len(product.featureSets) == 1        
        # Leerer Array ohne Varianten
        assert product.variants is not None
        assert len(product.variants) == 0
        # Keine Varianten gegeben
        assert product.hasVariants == False
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        assert product.numberOfVariants == 1

    def testAddFeatureSetSingleValueVariantFeature(self):
        # Single Feature, Single ValueVariant
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        variant = Variant()
        variant.productIdSuffix= "1L"
        variant.value = "Value" 
        feature.addVariant(variant)
        feature.addVariantOrder(1)
        featureSet.addFeature(feature)                
        assert len(product.featureSets) == 0
        product.addFeatureSet(featureSet)
        assert len(product.featureSets) == 1        
        # Leerer Array ohne Varianten
        assert product.variants is not None
        assert len(product.variants) == 1
        # Keine Varianten gegeben
        assert product.hasVariants == True
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        assert product.numberOfVariants == 1

    def testAddFeatureSetMultiValueVariantFeature(self):
        # Single Feature, Multi ValueVariant
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        variant = Variant()
        variant.productIdSuffix= "1L"
        variant.value = "Value" 
        feature.addVariant(variant)
        variant = Variant()
        variant.productIdSuffix= "2L"
        variant.value = "Value2" 
        feature.addVariant(variant)
        feature.addVariantOrder(1)
        featureSet.addFeature(feature)                
        assert len(product.featureSets) == 0
        product.addFeatureSet(featureSet)
        assert len(product.featureSets) == 1        
        # Array mit 1 Variante
        assert product.variants is not None
        assert len(product.variants) == 1
        # Varianten gegeben
        assert product.hasVariants == True
        # Anzahl der Varianten sollte 2 sein.
        assert product.numberOfVariants == 2


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    