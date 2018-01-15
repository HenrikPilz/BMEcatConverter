'''
Created on 15.01.2018

@author: henrik.pilz
'''
from xml.sax import make_parser
import os
import unittest

from datamodel import Feature
from datamodel import FeatureSet
from datamodel import Mime
from datamodel import OrderDetails
from datamodel import Price
from datamodel import PriceDetails
from datamodel import Product
from datamodel import ProductDetails
from datamodel import Reference
from datamodel import TreatmentClass
from importer.xml import BMEcatImportHandler
from resolver import DTDResolver


class XMLImportTest(unittest.TestCase):

    def testImportFromBMEcatFullDataPricenamesDifferent(self):
        inputFilename = "testImportFromBMEcatFullDataPricenamesDifferent.xml"
        article = self.__createFullArticle()
        importedArticle = self.__runImporter(inputFilename)
        self.__checkArticles(article, importedArticle)

    def __runImporter(self, filename):
        testDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "test_data")
        # import again
        parser = make_parser()
        importHandler = BMEcatImportHandler("%Y-%m-%d")
        parser.setContentHandler(importHandler)
        parser.setEntityResolver(DTDResolver())
        parser.parse("file:" + os.path.join(testDataPath, filename))
        return importHandler.articles['new'][0]

    def __createFullArticle(self):
        article = Product()
        article.productId = '12345'
        article.details = ProductDetails()
        article.details.deliveryTime = 10
        article.details.description = 'Test Description'
        article.details.ean = '12345678901234'
        article.details.keywords = [ 'Keyword 1', 'Keyword 2']
        article.details.manufacturerArticleId = '09876'
        article.details.manufacturerName = 'Manufacturer'
        tc = TreatmentClass()
        tc.classType = 'TestClass'
        tc.value = '12345'
        article.details.specialTreatmentClasses = [ tc ]
        article.details.title = '    Test Article    '
        article.details.supplierAltId = '23456'
        reference = Reference()
        reference.referenceType = 'accessory'
        reference.supplierArticleId = '09876'
        article.addReference(reference)
        # Bilder
        mime = Mime()
        mime.mimeType = 'image/jpg'
        mime.order = 1
        mime.purpose = 'detail'
        mime.source = 'manufacturer/Test.jpg'
        article.addMime(mime)
        mime = Mime()
        mime.mimeType = 'image/jpg'
        mime.order = 2
        mime.purpose = 'detail'
        mime.source = 'manufacturer/Test2.jpg'
        article.addMime(mime)
        mime = Mime()
        mime.mimeType = 'image/jpg'
        mime.order = 3
        mime.purpose = 'normal'
        mime.source = 'manufacturer/Test3.jpg'
        article.addMime(mime)
        # LieferDetails
        article.orderDetails = OrderDetails()
        article.orderDetails.contentUnit = 'C62'
        article.orderDetails.orderUnit = 'C62'
        article.orderDetails.packingQuantity = 25
        article.orderDetails.priceQuantity = 100
        article.orderDetails.quantityMin = 4
        article.orderDetails.quantityInterval = 1
        # Preise
        priceDetails = PriceDetails()
        price1 = Price()
        price1.amount = 10.50
        price1.priceType = 'EK_ohne_MWST'
        price1.lowerBound = 1
        price1.tax = 0.19
        priceDetails.addPrice(price1, False)
        price2 = Price()
        price2.amount = 17.50
        price2.priceType = 'UVP'
        price2.lowerBound = 1
        price2.tax = 0.19
        priceDetails.addPrice(price2, False)
        article.addPriceDetails(priceDetails, False)

        # Attribute
        featureSet = FeatureSet()
        feature = Feature()
        feature.name = "Test1"
        feature.addValue(10)
        featureSet.addFeature(feature)
        feature = Feature()
        feature.name = "Test2"
        feature.addValue("Blabla")
        featureSet.addFeature(feature)
        feature = Feature()
        feature.name = "Test3"
        feature.addValue("Blub")
        featureSet.addFeature(feature)
        feature = Feature()
        feature.name = "Test4"
        feature.addValue("Zack")
        featureSet.addFeature(feature)
        article.addFeatureSet(featureSet)
        return article

    def __checkArticles(self, article, article2):

        self.assertEqual(article.productId, article2.productId, "Artikelnummer")
        self.assertEqual(article.details.deliveryTime, int(article2.details.deliveryTime), "deliveryTime")
        self.assertEqual(article.details.ean, article2.details.ean, "ean")
        self.assertEqual(article.details.title.strip(), article2.details.title, "title")
        if article.details.description is not None:
            self.assertEqual(article.details.description.replace("\n", "<br>").strip(), article2.details.description, "description")
        else:
            self.assertEqual(article.details.description, article2.details.description, "description")
        if article.details.manufacturerArticleId is None and article2.details.manufacturerArticleId is not None:
            self.assertEqual(article.productId, article2.details.manufacturerArticleId, "manufacturerArticleId")
        else:
            self.assertEqual(article.details.manufacturerArticleId, article2.details.manufacturerArticleId, "manufacturerArticleId")

        self.assertEqual(article.details.manufacturerName, article2.details.manufacturerName, "manufacturerName")

        if len(article.details.keywords) > 0:
            self.assertEqual(article.details.keywords, article2.details.keywords, "keywords")
        if len(article.details.specialTreatmentClasses) > 0 and len(article2.details.specialTreatmentClasses) > 0:
            self.assertEqual(article.details.specialTreatmentClasses, article2.details.specialTreatmentClasses, "specialTreatmentClasses")

        self.assertEqual(article.details.erpGroupBuyer, article2.details.erpGroupBuyer, "erpGroupBuyer")
        self.assertEqual(article.details.erpGroupSupplier, article2.details.erpGroupSupplier, "erpGroupSupplier")
        self.assertEqual(article.details.remarks, article2.details.remarks, "remarks")
        self.assertEqual(article.details.buyerId, article2.details.buyerId, "buyerId")
        self.assertEqual(article.details.segment, article2.details.segment, "segment")
        self.assertEqual(article.details.articleOrder, article2.details.articleOrder, "articleOrder")
        self.assertEqual(article.details.articleStatus, article2.details.articleStatus, "articleStatus")
        if article.details.supplierAltId is not None and article2.details.supplierAltId is not None:
            self.assertEqual(article.details.supplierAltId, article2.details.supplierAltId, "supplierAltId")

        self.assertEqual(article.details.manufacturerTypeDescription, article2.details.manufacturerTypeDescription, "manufacturerTypeDescription")

        self.assertEqual(article.orderDetails, article2.orderDetails, "orderDetails")
        self.assertEqual(article.priceDetails, article2.priceDetails, "priceDetails")
        self.assertEqual(article.priceDetails[0], article2.priceDetails[0], "priceDetails[0]")

        self.assertEqual(len(article.featureSets), len(article2.featureSets), "len(featureSets)")
        if len(article.featureSets) > 0:
            self.assertEqual(len(article.featureSets[0]), len(article2.featureSets[0]), "len(featureSets[0])")
            self.assertEqual(article.featureSets[0].referenceSystem, article2.featureSets[0].referenceSystem, "featureSets.referenceSystem")
            self.assertEqual(article.featureSets[0].features[0].name, article2.featureSets[0].features[0].name, "feature[0].name")
            self.assertEqual(article.featureSets[0].features[0], article2.featureSets[0].features[0], "feature[0]")

            self.assertEqual(article.featureSets[0], article2.featureSets[0], "featureSet[0]")
        self.assertEqual(article.featureSets, article2.featureSets, "featureSets")
        self.assertEqual(article.mimeInfo, article2.mimeInfo, "mimeInfo")
        self.assertEqual(3, len(article2.mimeInfo), "mimeInfo")
        if len(article.references) > 0 and len(article2.references) > 0 :
            self.assertEqual(article.references, article2.references, "references")


# if __name__ == "__main__":
# import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
