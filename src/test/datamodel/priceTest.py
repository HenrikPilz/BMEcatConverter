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
        price.lowerBound = -1
        price.validate(True)
        price.lowerBound = 0
        price.validate(True)
        price.lowerBound = 1
        price.validate(True)
        price.currency = "USD"
        price.validate(True)
        price.currency = "EUR"
        price.validate(True)
        self.assertEqual(price.tax, 0.19, "Tax was not set when empty")
        price.tax = 0.17
        price.validate(True)
        self.assertEqual(price.tax, 0.19, "Tax was not set when false")
        price.tax = 0.07
        price.validate(True)
        self.assertEqual(price.tax, 0.07, "Tax was set but should stay")
        price.tax = "0.07"
        price.validate(True)
        self.assertEqual(price.tax, 0.07, "Tax was set but should stay")

    def testCeil(self):
        price = Price()
        price.amount = 1.335
        price.lowerBound = 1
        price.currency = "EUR"
        price.validate(True)
        self.assertEqual(price.amount, 1.34, "Ceil failed '{0}'".format(price.amount))

    def testFloor(self):
        price = Price()
        price.amount = 1.333
        price.lowerBound = 1
        price.currency = "EUR"
        price.validate(True)
        self.assertEqual(price.amount, 1.33, "Floor failed '{0}'".format(price.amount))

    def testEqual(self):
        price1 = Price()
        self.assertNotEqual(price1, "", "Prices should not be equal to str")

        price2 = Price()
        self.assertEqual(price1, price2, "Empty prices should be equal.")
        self.assertTrue(price1 == price2, "Empty prices should be equal via '=='.")
        self.assertFalse(price1 != price2, "Empty prices should not be unequal via '!='.")

        price1.amount = 1.0
        price2.amount = 1
        self.assertEqual(price1, price2, "Prices '1' and '1.0' should be equal.")

        price1.currency = "USD"
        price2.currency = "EUR"
        self.assertNotEqual(price1, price2, "Prices '1 EUR' and '1.0 USD' should not be equal.")
        price1.currency = "EUR"
        self.assertEqual(price1, price2, "Prices '1 EUR' and '1.0 EUR' should be equal.")

        price1.tax = 0.07
        price2.tax = 0.19
        self.assertNotEqual(price1, price2, "Prices '1 EUR' Tax 0.19 and '1.0 EUR' Tax 0.07 should not be equal.")
        price1.tax = 0.19
        self.assertEqual(price1, price2, "Prices '1 EUR' Tax 0.19 and '1.0 EUR' Tax 0.19 should be equal.")

        price1.lowerBound = 10
        price2.lowerBound = 1
        self.assertNotEqual(price1, price2, "Prices '1 EUR' min 1 and '1.0 EUR' for min 10 should not be equal.")
        price1.lowerBound = 1
        self.assertEqual(price1, price2, "Prices '1 EUR' and '1.0 EUR' should be equal for min 1.")

        price1.factor = 1.5
        price2.factor = 1.0
        self.assertNotEqual(price1, price2, "Prices '1 EUR'*1.0 and '1.0 EUR'*1.5 should not be equal.")
        price1.factor = 1.0
        self.assertEqual(price1, price2, "Prices '1 EUR' and '1.0 EUR' should be equal with same Factor.")

        price1.territory = "Deuschland"
        self.assertEqual(price1, price2, "Terrritory should not matter")

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
