'''
Created on 08.10.2017

@author: Henrik Pilz
'''

from datamodel import Product, ProductDetails, TreatmentClass, Mime, Reference, OrderDetails, Feature, Price, PriceDetails, FeatureSet
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
        # Keywords können in Excel noch nicht importiert werden.
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
        
    def testConvertAndReimportWithoutPrice(self):
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
        article.addPriceDetails(priceDetails)
        with self.assertRaisesRegex(Exception, "Der Artikel '12345' hat keine Preisinformationen."):
            super().runAndCheck(article, 'testConvertAndReimportWithoutPrice.xlsx')

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

    def testConvertAndReimportFullArticleWithFeatureMultipleValuesWithUnitSpace(self):
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
        feature.addValue("Zick")
        feature.addValue("Zack")
        feature.unit = " "
        featureSet.addFeature(feature)
        article.addFeatureSet(featureSet)

        self.__runMultipleValuesTestRoutine(article, 'testConvertAndReimportFullArticleWithFeatureMultipleValuesWithUnitSpace.xlsx')

    def testConvertAndReimportFullArticleWithFeatureMultipleValuesWithUnitNone(self):
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
        feature.addValue("Zick")
        feature.addValue("Zack")
        featureSet.addFeature(feature)
        article.addFeatureSet(featureSet)

        self.__runMultipleValuesTestRoutine(article, 'testConvertAndReimportFullArticleWithFeatureMultipleValuesWithUnitNone.xlsx')

    def testConvertAndReimportFullArticleWithFeatureMultipleValuesWithUnit(self):
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
        feature.addValue("Zick")
        feature.addValue("Zack")
        feature.unit = "Bam"
        featureSet.addFeature(feature)
        article.addFeatureSet(featureSet)

        self.__runMultipleValuesTestRoutine(article, 'testConvertAndReimportFullArticleWithFeatureMultipleValuesWithUnit.xlsx')
        
    def __runMultipleValuesTestRoutine(self, article, filename):
        article.validate(True)
        article2 = self.runTestMethod(article, filename )[0]


        self.assertEqual(article.productId, article2.productId, "Artikelnummer")
        self.assertEqual(article.details.deliveryTime, int(article2.details.deliveryTime), "deliveryTime")
        self.assertEqual(article.details.ean, article2.details.ean, "ean")
        self.assertEqual(article.details.title, article2.details.title, "title")
        self.assertEqual(article.details.description, article2.details.description, "description")
        self.assertEqual(article.details.manufacturerArticleId, article2.details.manufacturerArticleId, "manufacturerArticleId")

        self.assertEqual(article.details.manufacturerName, article2.details.manufacturerName, "manufacturerName")
           
        self.assertEqual(article.details.erpGroupBuyer, article2.details.erpGroupBuyer, "erpGroupBuyer")
        self.assertEqual(article.details.erpGroupSupplier, article2.details.erpGroupSupplier, "erpGroupSupplier")
        self.assertEqual(article.details.remarks, article2.details.remarks, "remarks")
        self.assertEqual(article.details.buyerId, article2.details.buyerId, "buyerId")
        self.assertEqual(article.details.segment, article2.details.segment, "segment")
        self.assertEqual(article.details.articleOrder, article2.details.articleOrder, "articleOrder")
        self.assertEqual(article.details.articleStatus, article2.details.articleStatus, "articleStatus")
            
        self.assertEqual(article.details.manufacturerTypeDescription, article2.details.manufacturerTypeDescription, "manufacturerTypeDescription")

        self.assertEqual(article.orderDetails, article2.orderDetails, "orderDetails")
        self.assertEqual(len(article.featureSets), len(article2.featureSets), "lean(featureSets)")
        # if len(article.featureSets) > 0:
        self.assertEqual(len(article.featureSets[0]), len(article2.featureSets[0]), "len(featureSets[0])")
        self.assertEqual(article.featureSets[0].referenceSytem, article2.featureSets[0].referenceSytem, "featureSets.referenceSytem")
        #    if len(article.featureSets[0].features) > 0:
        self.assertEqual(article.featureSets[0].features[0].name, article2.featureSets[0].features[0].name, "feature[0].name")
        feature1 = article.featureSets[0].features[0]
        newFeatureValue = feature1.values[0]
        if feature1.unit is not None:
            newFeatureValue += " " + feature1.unit 
        newFeatureValue = newFeatureValue.strip() + " | " + feature1.values[1]
        if feature1.unit is not None:
            newFeatureValue += " " + feature1.unit 
        self.assertEqual(newFeatureValue.strip(), article2.featureSets[0].features[0].values[0], "feature[0]")
            
        self.assertEqual(article.mimeInfo, article2.mimeInfo, "mimeInfo")
        # if len(article.references) > 0 and len(article2.references) > 0 :
        #    self.assertEqual(article.references, article2.references, "references")        
    
 
#if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
       
    