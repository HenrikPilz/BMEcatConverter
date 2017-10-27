'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import Price

class PriceTest(unittest.TestCase):

    def testInit(self):
        price = Price()
        self.assertIsNone(price.priceType)
        self.assertIsNone(price.amount)
        self.assertEqual(price.currency, "EUR")
        self.assertEqual(price.tax, 0.19)
        self.assertEqual(price.lowerBound, 1)
        self.assertIsNone(price.factor)
        self.assertIsNone(price.territory)

    def testValidateExceptionNoAmount(self):
        price = Price()
        with self.assertRaisesRegex(Exception, "Kein Preis angegeben!"): 
            price.validate(True)
        
    def testValidateExceptionNegativeAmount(self):
        price = Price()
        price.amount = -1.0
        with self.assertRaisesRegex(Exception, "Negativer Preis angegeben!"):
            price.validate(True)

    def testValidate(self):
        price = Price()
        price.amount = 1.0
        price.validate(True)

