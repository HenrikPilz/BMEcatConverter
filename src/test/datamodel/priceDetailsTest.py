'''
Created on 16.07.2017

@author: Henrik Pilz
'''
from datetime import datetime
import unittest

from lxml import etree

from datamodel import Price
from datamodel import PriceDetails


class PriceDetailsTest(unittest.TestCase):

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
        priceDetails.addPrice(Price(), False)
        with self.assertRaisesRegex(Exception, "Tagespreis hinterlegt!"):
            priceDetails.validate(True)

    def testAddPrice(self):
        priceDetails = PriceDetails()
        priceDetails.addPrice(None, True)
        self.assertListEqual(priceDetails.prices, [], "No Prices should have been added")
        priceDetails.addPrice(Price(), True)
        self.assertListEqual(priceDetails.prices, [], "No Prices should have been added")
        priceDetails.addPrice(Price(), False)
        self.assertListEqual(priceDetails.prices, [Price()], "Price should have been added")

    def testValidateExceptionMinOneMandatoryPriceMissing(self):
        priceDetails = PriceDetails()
        with self.assertRaisesRegex(Exception, "Keine Preisangaben hinterlegt."):
            priceDetails.validate(True)
        priceDetails.addPrice(Price(), False)

        with self.assertRaisesRegex(Exception, "Kein Preis angegeben!"):
            priceDetails.validate(True)

        priceDetails.prices = []
        price = Price()
        price.amount = 1
        price.priceType = "test"
        priceDetails.addPrice(price, True)
        with self.assertRaisesRegex(Exception, "Mindestens ein Pflichtpreis ist nicht vorhanden: 'net_customer'"):
            priceDetails.validate(True)

    def testValidateExceptionPriceTwice(self):
        priceDetails = PriceDetails()

        price = Price()
        price.amount = 1
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        self.assertEqual(len(priceDetails), 1, "Kein Preis hinzugefügt.")
        price = Price()
        price.amount = 3
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        self.assertEqual(len(priceDetails), 2, "Kein Preis hinzugefügt.")

        with self.assertRaisesRegex(Exception, "Jeder Preistyp darf nur einmal auftreten. Doppelt: 'net_customer'"):
            priceDetails.validate(True)

    def testValidate(self):
        priceDetails = PriceDetails()
        price = Price()
        price.amount = 1
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        priceDetails.validate(True)

    def testValidateWithValidityTimeSlice(self):
        priceDetails = PriceDetails()
        priceDetails.validFrom = datetime.strptime("2017-09-22", "%Y-%m-%d")
        priceDetails.validTo = datetime.strptime("2018-09-21", "%Y-%m-%d")

        price = Price()
        price.amount = 1
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        priceDetails.validate(True)

    def testValidateWithValidityTimeSliceNotCorrect(self):
        priceDetails = PriceDetails()
        priceDetails.validFrom = datetime.strptime("2018-09-22", "%Y-%m-%d")
        priceDetails.validTo = datetime.strptime("2018-09-21", "%Y-%m-%d")

        price = Price()
        price.amount = 1
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        priceDetails.validate(True)

    def testEqual(self):
        priceDetails1 = PriceDetails()
        self.assertNotEqual(priceDetails1, "", "PriceDetails should not be equal to str")

        priceDetails2 = PriceDetails()
        self.assertEqual(priceDetails1, priceDetails2, "Empty priceDetails should be equal.")
        self.assertTrue(priceDetails1 == priceDetails2, "Empty priceDetails should be equal via '=='.")
        self.assertFalse(priceDetails1 != priceDetails2, "Empty priceDetails should not be unequal via '!='.")

        priceDetails1.dailyPrice = True
        self.assertNotEqual(priceDetails1, priceDetails2, "priceDetails 'dailyPrice' and 'not dailyPrice' should not be equal.")
        priceDetails1.dailyPrice = None
        self.assertEqual(priceDetails1, priceDetails2, "priceDetails 'dailyPrice' and 'dailyPrice' should be equal.")

        priceDetails1.validFrom = "2017-08-20"
        self.assertNotEqual(priceDetails1, priceDetails2, "priceDetails different startingdays should not be equal.")
        priceDetails2.validFrom = "2017-08-20"
        self.assertEqual(priceDetails1, priceDetails2, "Same Starting day priceDetails should be equal.")

        priceDetails1.validTo = "2017-08-21"
        self.assertNotEqual(priceDetails1, priceDetails2, "priceDetails different startingdays should not be equal.")
        priceDetails2.validTo = "2017-08-21"
        self.assertEqual(priceDetails1, priceDetails2, "Same Starting day priceDetails should be equal.")

    def testToXml(self):
        priceDetails = PriceDetails()
        priceDetails.validFrom = datetime.strptime("2017-09-22", "%Y-%m-%d")
        priceDetails.validTo = datetime.strptime("2018-09-21", "%Y-%m-%d")

        price = Price()
        price.amount = 1
        price.priceType = "net_customer"
        priceDetails.addPrice(price, True)
        self.assertEqual(etree.tostring(priceDetails.toXml()),
                         b'<ARTICLE_PRICE_DETAILS>' +
                         b'<DATETIME type="valid_start_date"><DATE>2017-09-22</DATE><TIME>00:00:00</TIME></DATETIME>' +
                         b'<DATETIME type="valid_end_date"><DATE>2018-09-21</DATE><TIME>00:00:00</TIME></DATETIME>' +
                         b'<ARTICLE_PRICE price_type="net_customer"><PRICE_AMOUNT>1.0</PRICE_AMOUNT><PRICE_CURRENCY>EUR</PRICE_CURRENCY>' +
                         b'<TAX>0.19</TAX><LOWER_BOUND>1</LOWER_BOUND></ARTICLE_PRICE></ARTICLE_PRICE_DETAILS>',
                         "XML Output Kaputt")


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
