'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.price import Price

class TestPrice(unittest.TestCase):

    def testInit(self):
        price = Price()
        assert price.priceType == None
        assert price.amount == None
        assert price.currency == "EUR"
        assert price.tax == 0.19
        assert price.lowerBound == 1
        assert price.factor == 1.0
        assert price.territory == "DEU"

    def testValidateExceptionNoAmount(self):
        price = Price()
        try:
            price.validate(True)
        except Exception as ve:
            assert ve == "Kein Preis angegeben!"
        
    def testValidateExceptionNegativeAmount(self):
        price = Price()
        price.amount = -1.0
        try:
            price.validate(True)
        except Exception as ve:
            assert ve == "Negativer Preis angegeben!"

    def testValidate(self):
        price = Price()
        price.amount = 1.0
        price.validate()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    