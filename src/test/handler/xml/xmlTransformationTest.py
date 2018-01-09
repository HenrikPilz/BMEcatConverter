'''
Created on 09.10.2017

@author: Henrik Pilz
'''
from xml.sax import make_parser
import os

from datamodel import Feature, FeatureSet, Mime, OrderDetails, Price, PriceDetails, Product, ProductDetails, Reference, TreatmentClass
from exporter.xml.bmecatExporter import BMEcatExporter
from importer.xml.bmecatImportHandler import BMEcatImportHandler
from resolver import DTDResolver
from test.handler.basicHandlerTest import BasicHandlerTest


class XmlTransformationNonFiegeTest(BasicHandlerTest):

    def testCreateBMEcatFullData(self):
        article = Product()
        article.productId = '12345'
        article.details = ProductDetails()
        article.details.deliveryTime = 10
        article.details.description = 'Test Description\nTest Descirption Line 2   '
        article.details.ean = '12345678901234'
        article.details.keywords = [ 'Keyword 1', 'Keyword 2']
        article.details.manufacturerArticleId = '09876'
        article.details.manufacturerName = 'Manufacturer'
        article.details.articleStatus = "Bla"
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
        price1.priceType = 'net_customer'
        price1.lowerBound = 1
        price1.tax = 0.19
        priceDetails.addPrice(price1)
        price2 = Price()
        price2.amount = 17.50
        price2.priceType = 'net_list'
        price2.lowerBound = 1
        price2.tax = 0.19
        priceDetails.addPrice(price2)
        article.addPriceDetails(priceDetails)

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

        self.runAndCheck(article, 'testCreateBMEcatFullData.xml', 'contorion')

    def testCreateBMEcatMinimumDataPlusKeywords(self):
        article = Product()
        article.productId = '12345'
        article.details = ProductDetails()
        article.details.title = 'Test Article'
        article.orderDetails = OrderDetails()
        article.orderDetails.contentUnit = 'C62'
        article.orderDetails.orderUnit = 'C62'
        article.orderDetails.packingQuantity = 25
        article.orderDetails.priceQuantity = 100
        article.orderDetails.quantityMin = 4
        article.orderDetails.quantityInterval = 1

        priceDetails = PriceDetails()
        price = Price()
        price.amount = 10.50
        price.priceType = 'net_customer'
        price.lowerBound = 1
        price.tax = 0.19
        priceDetails.addPrice(price)
        article.addPriceDetails(priceDetails)

        article.addKeyword("Testkeyword")

        self.runAndCheck(article, 'testCreateBMEcatMinimumDataPlusKeywords.xml', 'contorion')

    def testCreateBMEcatMinimumDataFloatDescription(self):
        article = Product()
        article.productId = '12345'
        article.details = ProductDetails()
        article.details.title = 'Test Article'
        article.details.description = 123.567
        article.orderDetails = OrderDetails()
        article.orderDetails.contentUnit = 'C62'
        article.orderDetails.orderUnit = 'C62'
        article.orderDetails.packingQuantity = 25
        article.orderDetails.priceQuantity = 100
        article.orderDetails.quantityMin = 4
        article.orderDetails.quantityInterval = 1

        priceDetails = PriceDetails()
        price = Price()
        price.amount = 10.50
        price.priceType = 'net_customer'
        price.lowerBound = 1
        price.tax = 0.19
        priceDetails.addPrice(price)
        article.addPriceDetails(priceDetails)
        self.runAndCheck(article, 'testCreateBMEcatMinimumDataFloatDescription.xml', 'contorion')

    def testCreateBMEcatMinimumData(self):
        article = Product()
        article.productId = '12345'
        article.details = ProductDetails()
        article.details.title = 'Test Article'
        article.orderDetails = OrderDetails()
        article.orderDetails.contentUnit = 'C62'
        article.orderDetails.orderUnit = 'C62'
        article.orderDetails.packingQuantity = 25
        article.orderDetails.priceQuantity = 100
        article.orderDetails.quantityMin = 4
        article.orderDetails.quantityInterval = 1

        priceDetails = PriceDetails()
        price = Price()
        price.amount = 10.50
        price.priceType = 'net_customer'
        price.lowerBound = 1
        price.tax = 0.19
        priceDetails.addPrice(price)
        article.addPriceDetails(priceDetails)
        self.runAndCheck(article, 'testCreateBMEcatMinimumData.xml', 'contorion')

    def runTestMethod(self, article, filename, merchant='contorion'):
        articles = { 'new' : [ article ]}

        # export
        bmecatExporter = BMEcatExporter(articles, filename, merchant)
        bmecatExporter.writeBMEcatAsXML()

        # import again
        parser = make_parser()
        importHandler = BMEcatImportHandler("%Y-%m-%d")
        parser.setContentHandler(importHandler)
        parser.setEntityResolver(DTDResolver())
        parser.parse("file:" + filename)
        return importHandler.articles['new']


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
