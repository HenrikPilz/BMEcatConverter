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
from data.orderDetails import OrderDetails
from data.priceDetails import PriceDetails


class TestProduct(unittest.TestCase):

    def testInit(self):
        product = Product()
        # Default: keine ProductID
        self.assertIsNone(product.productId)
        # keine Details
        self.assertIsNone(product.details)
        # keine OrderDetails
        self.assertIsNone(product.orderDetails)
        # Leerer Array ohne Preisdetails
        self.assertIsNotNone(product.priceDetails)
        self.assertEqual(len(product.priceDetails),0)
        # Leerer Array ohne Bilder
        self.assertIsNotNone(product.mimeInfo)
        self.assertEqual(len(product.mimeInfo),0)
        # Leerer Array ohne Attribute
        self.assertIsNotNone(product.featureSets)
        self.assertEqual(len(product.featureSets),0)
        # Leerer Array ohne Referenzen
        self.assertIsNotNone(product.references)
        self.assertEqual(len(product.references),0)
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants),0)
        # Leerer Array ohne UserDefinedExtensions
        self.assertIsNotNone(product.userDefinedExtensions)
        self.assertEqual(len(product.userDefinedExtensions.keys()),0)
        # Keine Varianten gegeben
        self.assertFalse(product.hasVariants)
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        self.assertEqual(product.numberOfVariants,1)

    def testDetails(self):
        product = Product()
        
        # setzen der Product ID       
        product.productId = "12345"
        self.assertEqual(product.productId, "12345")
        # Productdetails
        product.details = ProductDetails()
        
        product.addTitle("TestTitel")
        self.assertEqual(product.details.title, "TestTitel")
        
        product.addDescription("TestBeschreibung")
        self.assertEqual(product.details.description, "TestBeschreibung")

        product.addManufacturerArticleId("12345")
        self.assertEqual(product.details.manufacturerArticleId,"12345")

        product.addManufacturerName("Test")
        self.assertEqual(product.details.manufacturerName, "Test")

        product.addEAN("1234567890123")
        self.assertEqual(product.details.ean, "1234567890123")

        product.addDeliveryTime(2)
        self.assertEqual(product.details.deliveryTime,2)

        self.assertEqual(len(product.details.keywords),0)
        product.addKeyword("TestKeyword")
        self.assertEqual(len(product.details.keywords),1)
        self.assertIn("TestKeyword", product.details.keywords)

        self.assertEqual(len(product.details.specialTreatmentClasses),0)
        product.addSpecialTreatmentClass("TestClass")
        self.assertEqual(len(product.details.specialTreatmentClasses),1)
        self.assertIn("TestClass", product.details.specialTreatmentClasses)

    def testAddMime(self):
        product = Product()
        self.assertEqual(len(product.mimeInfo),0)
        product.addMime(Mime())
        self.assertEqual(len(product.mimeInfo),1)        
            
    def testAddReference(self):
        product = Product()
        self.assertEqual(len(product.references),0)
        product.addReference(Reference())
        self.assertEqual(len(product.references),1)        

    def testAddUserDefinedExtension(self):
        product = Product()
        self.assertEqual(len(product.userDefinedExtensions),0)
        product.addUserDefinedExtension("")
        self.assertEqual(len(product.userDefinedExtensions),0)
        # Aktuell passiert hier noch nichts        

    def testAddFeatureSetSingleValueFeature(self):
        # Single Feature, Single Value per Feature
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet.addFeature(feature)                
        self.assertEqual(len(product.featureSets),0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets),1)        
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants),0)
        # Keine Varianten gegeben
        self.assertFalse(product.hasVariants)
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        self.assertEqual(product.numberOfVariants,1)

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
        self.assertEqual(len(product.featureSets),0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets),1)        
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants),1)
        # Keine Varianten gegeben
        self.assertTrue(product.hasVariants)
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        self.assertEqual(product.numberOfVariants,1)

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
        self.assertEqual(len(product.featureSets),0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets),1)        
        # Array mit 1 Variante
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants),1)
        # Varianten gegeben
        self.assertTrue(product.hasVariants)
        # Anzahl der Varianten sollte 2 sein.
        self.assertEqual(product.numberOfVariants,2)
        
    def testValidateExceptionNoArticleNumber(self):
        product = Product()
        with self.assertRaisesRegex(Exception, "Der Artikel hat keine Artikelnummer."):
            product.validate(True)

    def testValidateExceptionNoArticleDetails(self):
        product = Product()
        # setzen der Product ID       
        product.productId = "12345"
        with self.assertRaisesRegex(Exception, "Der Artikel hat keine Artikeldetails."):
            product.validate(True)
        # Productdetails
        product.details = ProductDetails()
        with self.assertRaisesRegex(Exception, "Ein Artikelname fehlt"):
            product.validate(True)

    def testValidateExceptionNoOrderDetails(self):
        product = Product()
        # setzen der Product ID       
        product.productId = "12345"
        
        # Productdetails
        product.details = ProductDetails()
        product.addTitle("TestTitel")

        with self.assertRaisesRegex(Exception, "Der Artikel hat keine Bestellinformation."):
            product.validate(True)
    
    def testValidateExceptionNoPriceInformation(self):
        product = Product()
        # setzen der Product ID       
        product.productId = "12345"
        
        # Productdetails
        product.details = ProductDetails()
        product.addTitle("TestTitel")

        orderDetails = OrderDetails()
        orderDetails.orderUnit = "C62"
        orderDetails.contentUnit = "C62"

        product.orderDetails = orderDetails
        
        with self.assertRaisesRegex(Exception, "Der Artikel hat keine Preisinformationen."):
            product.validate(True)

        product.priceDetails = None
        with self.assertRaisesRegex(Exception, "Der Artikel hat keine Preisinformationen."):
            product.validate(True)



    def testValidate(self):
        product = Product()
        # setzen der Product ID       
        product.productId = "12345"
        
        # Productdetails
        product.details = ProductDetails()
        product.addTitle("TestTitel")

        orderDetails = OrderDetails()
        orderDetails.orderUnit = "C62"
        orderDetails.contentUnit = "C62"

        product.orderDetails = orderDetails
        
        priceDetails = PriceDetails()
        product.addPriceDetails(priceDetails)
        product.validate(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    