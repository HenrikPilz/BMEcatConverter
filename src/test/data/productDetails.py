'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.productDetails import ProductDetails

class TestProductDetails(unittest.TestCase):

    def testInit(self):
        productdetails = ProductDetails()
        self.assertIsNone(productdetails.title)
        self.assertIsNone(productdetails.description)
        self.assertIsNone(productdetails.manufacturerTypeDescription)
        self.assertIsNone(productdetails.ean)
        self.assertIsNone(productdetails.supplierAltId)
        self.assertIsNone(productdetails.buyerId)
        self.assertIsNone(productdetails.manufacturerArticleId)
        self.assertIsNone(productdetails.manufacturerName)
        self.assertIsNone(productdetails.erpGroupBuyer)
        self.assertIsNone(productdetails.erpGroupSupplier)
        self.assertEqual(productdetails.deliveryTime, 2)
        self.assertIsNotNone(productdetails.specialTreatmentClasses)
        self.assertEqual(len(productdetails.specialTreatmentClasses), 0)
        self.assertIsNotNone(productdetails.keywords)
        self.assertEqual(len(productdetails.keywords), 0)
        self.assertIsNotNone(productdetails.remarks)
        self.assertEqual(len(productdetails.remarks), 0)
        self.assertIsNotNone(productdetails.segment)
        self.assertEqual(len(productdetails.segment), 0)
                             
        self.assertEqual(productdetails.articleOrder, 1)
        self.assertIsNone(productdetails.articleStatus)  

    def testAddSpecialTreatmentClass(self):
        productdetails = ProductDetails()
        self.assertEqual(len(productdetails.specialTreatmentClasses), 0)
        productdetails.addSpecialTreatmentClass("Test")
        self.assertEqual(len(productdetails.specialTreatmentClasses), 1)
    
    def testAddKeyword(self,):
        productdetails = ProductDetails()
        self.assertEqual(len(productdetails.keywords), 0)
        productdetails.addKeyword("Test")
        self.assertEqual(len(productdetails.keywords), 1)

    def testValidateExceptionNoArticleTitle(self):
        productdetails = ProductDetails()
        with self.assertRaisesRegex(Exception, "Ein Artikelname fehlt"):
            productdetails.validate(True)

    def testValidate(self):
        productdetails = ProductDetails()
        productdetails.title = "Test"
        productdetails.validate(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    