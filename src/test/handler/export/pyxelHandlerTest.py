'''
Created on 08.10.2017

@author: Henrik Pilz
'''

from data import Product, ProductDetails, TreatmentClass, Mime, Reference, OrderDetails, Feature, Price, PriceDetails
from data.featureSet import FeatureSet
from exporter.excel import PyxelExporter
from importer.excel import ExcelImporter
from test.handler.basicHandlerTest import BasicHandlerTest


class PyxelHandlerTest(BasicHandlerTest):

    def testConvertAndReimportFullArticle(self):
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
        mime.source = 'manufacturer/Test1.jpg'
        article.addMime(mime)
        mime = Mime()
        mime.mimeType = 'image/jpg'
        mime.order = 2
        mime.purpose = 'detail'
        mime.source = 'manufacturer/Test2.jpg'
        article.addMime(mime)
        # Bestelldetails
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

        super().runAndCheck(article, 'testConvertAndReimportFullArticle.xlsx')
        
    def testConvertAndReimportWithManufacturerArticleId(self):
        article = Product()
        article.productId = '12345'
        article.details = ProductDetails()
        article.details.manufacturerArticleId = '09876'
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
        super().runAndCheck(article, 'testConvertAndReimportWithManufacturerArticleId.xlsx')

    def testConvertAndReimportWithoutManufacturerArticleId(self):
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
        super().runAndCheck(article, 'testConvertAndReimportWithoutManufacturerArticleId.xlsx')

    def runTestMethod(self, article, filename):        
        articles = { 'new' : [ article ]}

        # export as Excel
        pyxelHandler = PyxelExporter(articles, filename)
        pyxelHandler.createNewWorkbook()

        # import again
        excelImporter = ExcelImporter()
        excelImporter.readWorkbook(filename)
        
        return excelImporter.articles
