'''
Created on 08.10.2017

@author: Henrik Pilz
'''
import unittest
from exportHandler.excel.pyxelHandler import PyxelHandler
from data import Product, ProductDetails, TreatmentClass, Mime, Reference, OrderDetails, Feature, Price, PriceDetails
from importHandler.excel.excelImporter import ExcelImporter

class PyxelHandlerTest(unittest.TestCase):

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
        
        mime = Mime()
        mime.mimeType = 'image/jpg'
        mime.order = 1
        mime.purpose = 'detail'
        mime.source = 'manufacturer/Test.jpg'
        article.addMime(mime)
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
        self.__runAndCheck(article)
        
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
        self.__runAndCheck(article)

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
        self.__runAndCheck(article)

    def __runAndCheck(self, article):        
        article.validate(True)
        articles = { 'new' : [ article ]}
        
        pyxelHandler = PyxelHandler(articles, 'test_excel_output.xlsx')
        
        pyxelHandler.createNewWorkbook()


        excelImporter = ExcelImporter()
        excelImporter.readWorkbook('test_excel_output.xlsx')
        
        article2 = excelImporter.articles[0]

        self.assertEqual(article.productId, article2.productId, "Artikelnummer")
        self.assertEqual(article.details.deliveryTime, article2.details.deliveryTime, "deliveryTime")
        self.assertEqual(article.details.ean, article2.details.ean, "ean")
        self.assertEqual(article.details.title, article2.details.title, "title")
        self.assertEqual(article.details.description, article2.details.description, "description")
        if article.details.manufacturerArticleId is None:
            self.assertEqual(article.productId, article2.details.manufacturerArticleId, "manufacturerArticleId")
        else:
            self.assertEqual(article.details.manufacturerArticleId, article2.details.manufacturerArticleId, "manufacturerArticleId")
        self.assertEqual(article.details.manufacturerName, article2.details.manufacturerName, "manufacturerName")
        #self.assertEqual(article.details.keywords, article2.details.keywords, "keywords")
        #self.assertEqual(article.details.specialTreatmentClasses, article2.details.specialTreatmentClasses, "specialTreatmentClasses")
        self.assertEqual(article.details.erpGroupBuyer, article2.details.erpGroupBuyer, "erpGroupBuyer")
        self.assertEqual(article.details.erpGroupSupplier, article2.details.erpGroupSupplier, "erpGroupSupplier")
        self.assertEqual(article.details.remarks, article2.details.remarks, "remarks")
        self.assertEqual(article.details.buyerId, article2.details.buyerId, "buyerId")
        self.assertEqual(article.details.segment, article2.details.segment, "segment")
        self.assertEqual(article.details.articleOrder, article2.details.articleOrder, "articleOrder")
        self.assertEqual(article.details.articleStatus, article2.details.articleStatus, "articleStatus")
        #self.assertEqual(article.details.supplierAltId, article2.details.supplierAltId, "supplierAltId")
        self.assertEqual(article.details.manufacturerTypeDescription, article2.details.manufacturerTypeDescription, "manufacturerTypeDescription")
        self.assertEqual(article.orderDetails, article2.orderDetails, "orderDetails")
        self.assertEqual(article.featureSets, article2.featureSets, "featureSets")
        self.assertEqual(article.mimeInfo, article2.mimeInfo, "mimeInfo")
        #self.assertEqual(article.references, article2.references, "references")        
