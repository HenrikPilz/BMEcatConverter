'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.priceDetails import PriceDetails

class TestPriceDetails(unittest.TestCase):

    def testInit(self):
        priceDetails = PriceDetails()
        
        self.assertIsNone(priceDetails.validFrom)
        self.assertIsNone(priceDetails.validTo)
        self.assertFalse(priceDetails.dailyPrice)
        self.assertIsNotNone(priceDetails.prices)
        self.assertEqual(len(priceDetails.prices), 0)

    def testValidateExceptionDailyPrice(self):
        priceDetails = PriceDetails()
        priceDetails.dailyPrice = True
        with self.assertRaisesRegex(Exception, "Tagespreis hinterlegt!"):
            priceDetails.validate(True)
                
            

    def testValidate(self):
        priceDetails = PriceDetails()
        priceDetails.validate(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    