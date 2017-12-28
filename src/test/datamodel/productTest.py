'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import Feature, FeatureSet, Mime, Product, ProductDetails, Reference, Variant, OrderDetails, PriceDetails, Price
from datamodel.treatmentClass import TreatmentClass


class ProductTest(unittest.TestCase):

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
        self.assertEqual(len(product.priceDetails), 0)
        # Leerer Array ohne Bilder
        self.assertIsNotNone(product.mimeInfo)
        self.assertEqual(len(product.mimeInfo), 0)
        # Leerer Array ohne Attribute
        self.assertIsNotNone(product.featureSets)
        self.assertEqual(len(product.featureSets), 0)
        # Leerer Array ohne Referenzen
        self.assertIsNotNone(product.references)
        self.assertEqual(len(product.references), 0)
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants), 0)
        # Leerer Array ohne UserDefinedExtensions
        self.assertIsNotNone(product.userDefinedExtensions)
        self.assertEqual(len(product.userDefinedExtensions.keys()), 0)
        # Keine Varianten gegeben
        self.assertFalse(product.hasVariants)
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        self.assertEqual(product.numberOfVariants, 1)

    def testDetails(self):
        product = Product()

        # setzen der Product ID
        product.productId = "12345"
        self.assertEqual(product.productId, "12345")
        # Productdetails
        product.addDetails()

        product.details.title = "TestTitel"
        self.assertEqual(product.details.title, "TestTitel")
        product.addDetails()
        self.assertEqual(product.details.title, "TestTitel")

        product.details.description = "TestBeschreibung"
        self.assertEqual(product.details.description, "TestBeschreibung")

        product.details.manufacturerArticleId = "12345"
        self.assertEqual(product.details.manufacturerArticleId, "12345")

        product.details.manufacturerName = "Test"
        self.assertEqual(product.details.manufacturerName, "Test")

        product.details.ean = "1234567890123"
        self.assertEqual(product.details.ean, "1234567890123")

        product.details.deliveryTime = 2
        self.assertEqual(product.details.deliveryTime, 2)

        self.assertEqual(len(product.details.keywords), 0)
        product.addKeyword("TestKeyword")
        self.assertEqual(len(product.details.keywords), 1)
        self.assertIn("TestKeyword", product.details.keywords)

        self.assertEqual(len(product.details.specialTreatmentClasses), 0)
        product.addSpecialTreatmentClass(TreatmentClass())
        self.assertEqual(len(product.details.specialTreatmentClasses), 0)
        treatmentclass = TreatmentClass()
        treatmentclass.classType = "CType"
        treatmentclass.value = "CValue"
        product.addSpecialTreatmentClass(treatmentclass)
        self.assertEqual(len(product.details.specialTreatmentClasses), 1)
        self.assertIn(treatmentclass, product.details.specialTreatmentClasses)

    def testAddMimeFailed(self):
        product = Product()
        mime = Mime()
        self.assertEqual(len(product.mimeInfo), 0)
        product.addMime(mime)
        self.assertEqual(len(product.mimeInfo), 0)
        mime.source = "asdfhjk.jpg"
        product.addMime(mime)
        self.assertEqual(len(product.mimeInfo), 0)
        mime.mimeType = "image/jpg"
        product.addMime(mime)
        self.assertEqual(len(product.mimeInfo), 0)
        mime.order = 1
        product.addMime(mime)
        self.assertEqual(len(product.mimeInfo), 0)

    def testAddMimeDetermineOrder(self):
        product = Product()
        mime = Mime()
        mime.source = "test.jpg"
        mime.mimeType = "image/jpg"
        mime.purpose = "detail"
        self.assertEqual(len(product.mimeInfo), 0)
        product.addMime(mime)
        self.assertEqual(len(product.mimeInfo), 1)
        self.assertEqual(product.mimeInfo[0].order, 1)

    def testAddMimePresetOrder(self):
        product = Product()
        mime = Mime()
        mime.source = "test.jpg"
        mime.mimeType = "image/jpg"
        mime.purpose = "detail"
        mime.order = 3
        self.assertEqual(len(product.mimeInfo), 0)
        product.addMime(mime)
        self.assertEqual(len(product.mimeInfo), 1)
        self.assertEqual(product.mimeInfo[0].order, 3)

    def testAddReference(self):
        product = Product()
        self.assertEqual(len(product.references), 0)
        product.addReference(Reference())
        self.assertEqual(len(product.references), 0)
        reference = Reference()
        reference.referenceType = "sparepart"
        reference.addSupplierArticleId("Test")
        product.addReference(reference)
        self.assertEqual(len(product.references), 1)

    def testAddUserDefinedExtension(self):
        product = Product()
        self.assertEqual(len(product.userDefinedExtensions), 0)
        product.addUserDefinedExtension("")
        self.assertEqual(len(product.userDefinedExtensions), 0)
        # Aktuell passiert hier noch nichts

    def testAddFeatureSetOnBlacklist(self):
        # Single Feature, Single Value per Feature
        product = Product()
        featureSet = FeatureSet()
        featureSet.referenceSystem = "PCLASS-6.0"
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet.addFeature(feature)
        self.assertEqual(len(product.featureSets), 0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets), 0)
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants), 0)
        # Keine Varianten gegeben
        self.assertFalse(product.hasVariants)

    def testAddFeatureSetSingleValueFeature(self):
        # Single Feature, Single Value per Feature
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        feature.addValue("Value")
        featureSet.addFeature(feature)
        self.assertEqual(len(product.featureSets), 0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets), 1)
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants), 0)
        # Keine Varianten gegeben
        self.assertFalse(product.hasVariants)
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        self.assertEqual(product.numberOfVariants, 1)

    def testAddFeatureSetSingleValueVariantFeature(self):
        # Single Feature, Single ValueVariant
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        variant = Variant()
        variant.productIdSuffix = "1L"
        variant.value = "Value"
        feature.addVariant(variant)
        feature.addVariantOrder(1)
        featureSet.addFeature(feature)
        self.assertEqual(len(product.featureSets), 0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets), 1)
        # Leerer Array ohne Varianten
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants), 0)
        # Keine Varianten gegeben
        self.assertFalse(product.hasVariants)
        # Anzahl der Varianten ist mindestens 1, da der Artikel selber auch eine Variante darstellt.
        self.assertEqual(product.numberOfVariants, 1)

    def testAddFeatureSetMultiValueVariantFeature(self):
        # Single Feature, Multi ValueVariant
        product = Product()
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Name"
        variant = Variant()
        variant.productIdSuffix = "1L"
        variant.value = "Value"
        feature.addVariant(variant)
        variant = Variant()
        variant.productIdSuffix = "2L"
        variant.value = "Value2"
        feature.addVariant(variant)
        feature.addVariantOrder(1)
        featureSet.addFeature(feature)
        self.assertEqual(len(product.featureSets), 0)
        product.addFeatureSet(featureSet)
        self.assertEqual(len(product.featureSets), 1)
        # Array mit 1 Variante
        self.assertIsNotNone(product.variants)
        self.assertEqual(len(product.variants), 1)
        # Varianten gegeben
        self.assertTrue(product.hasVariants)
        # Anzahl der Varianten sollte 2 sein.
        self.assertEqual(product.numberOfVariants, 2)

    def testValidateExceptionNoArticleNumber(self):
        product = Product()
        with self.assertRaisesRegex(Exception, "Der Artikel hat keine Artikelnummer."):
            product.validate(True)

    def testValidateExceptionNoArticleDetails(self):
        product = Product()
        # setzen der Product ID
        product.productId = "12345"
        with self.assertRaisesRegex(Exception, "Der Artikel '[0-9]{5}' hat keine Artikeldetails."):
            product.validate(True)
        # Productdetails
        product.addDetails()
        with self.assertRaisesRegex(Exception, "Ein Artikelname fehlt"):
            product.validate(True)

    def testValidateExceptionNoOrderDetails(self):
        product = Product()
        # setzen der Product ID
        product.productId = "12345"

        # Productdetails
        product.addDetails()
        product.details.title = "TestTitel"

        with self.assertRaisesRegex(Exception, "Der Artikel '[0-9]{5}' hat keine Bestellinformation."):
            product.validate(True)

    def testValidateExceptionNoPriceInformation(self):
        product = Product()
        # setzen der Product ID
        product.productId = "12345"

        # Productdetails
        product.details = ProductDetails()
        product.details.title = "TestTitel"

        product.addOrderDetails()
        product.orderDetails.orderUnit = "C62"
        product.orderDetails.contentUnit = "C62"

        product.orderDetails.packingQuantity = 1
        product.orderDetails.priceQuantity = 1
        product.orderDetails.quantityInterval = 1
        product.orderDetails.quantityMin = 1

        with self.assertRaisesRegex(Exception, "Der Artikel '[0-9]{5}' hat keine Preisinformationen."):
            product.validate(True)

        product.priceDetails = None
        with self.assertRaisesRegex(Exception, "Der Artikel '[0-9]{5}' hat keine Preisinformationen."):
            product.validate(True)

    def testValidate(self):
        product = Product()
        # setzen der Product ID
        product.productId = "12345 "
        self.assertEqual(product.productId, "12345 ")

        # Productdetails
        product.addDetails()
        product.details.title = "TestTitel"

        orderDetails = OrderDetails()
        orderDetails.orderUnit = "C62"
        orderDetails.contentUnit = "C62"
        orderDetails.packingQuantity = 1
        orderDetails.priceQuantity = 1
        orderDetails.quantityInterval = 1
        orderDetails.quantityMin = 1

        product.orderDetails = orderDetails

        priceDetails = PriceDetails()
        price = Price()
        price.amount = 1
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        product.addPriceDetails(priceDetails)
        product.validate(True)
        self.assertEqual(product.productId, "12345")
        product.addOrderDetails()
        product.validate(True)

    def testEqual(self):
        product1 = Product()
        self.assertNotEqual(product1, None, "Product not equal to None")
        self.assertNotEqual(product1, "", "Product not equal to str")

        product2 = Product()

        self.assertEqual(product1, product2, "Empty Products should be equal")
        self.assertTrue(product1 == product2, "Empty Products should be equal via '==")
        self.assertFalse(product1 != product2, "Empty Products should not be nonequal via '!='")

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
