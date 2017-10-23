'''
Created on 09.10.2017

@author: Henrik Pilz
'''
from xml.sax import make_parser

from data import Feature, FeatureSet, Mime, OrderDetails, Price, PriceDetails, Product, ProductDetails, Reference, TreatmentClass
from exportHandler.xml import BMEcatHandler as BMEcatExporter
from importHandler.xml import BMEcatHandler as BMEcatImporter
from resolver import DTDResolver
from test.handler.basicHandlerTest import BasicHandlerTest


class xmlHandlerTest(BasicHandlerTest):

    def testCreateBMEcatFullData(self):
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
        article.details.title = 'Test Article'
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
        price = Price()
        price.amount = 10.50
        price.priceType ='net_customer'
        price.lowerBound = 1
        price.tax = 0.19
        priceDetails.addPrice(price)
        article.addPriceDetails(priceDetails)
        price = Price()
        price.amount = 17.50
        price.priceType ='net_list'
        price.lowerBound = 1
        price.tax = 0.19
        priceDetails.addPrice(price)
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

        self.runAndCheck(article, 'testCreateBMEcatFullData.xml')
        
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
        price.priceType ='net_customer'
        price.lowerBound = 1
        price.tax = 0.19
        priceDetails.addPrice(price)
        article.addPriceDetails(priceDetails)
        self.runAndCheck(article, 'testCreateBMEcatMinimumData.xml')
        
    def runTestMethod(self, article, filename):   
        articles = { 'new' : [ article ]}
        # export
        bmecatExporter = BMEcatExporter(articles, filename)
        bmecatExporter.writeBMEcatAsXML()
        
        # import again
        parser = make_parser()
        importer = BMEcatImporter("%Y-%m-%d", ".", ",")
        parser.setContentHandler(importer)
        parser.setEntityResolver(DTDResolver())
        parser.parse("file:" + filename)
        return importer.articles['new']
