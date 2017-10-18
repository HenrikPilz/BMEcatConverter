'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingObject, XmlObject, ComparableEqual
from lxml.etree import Element

class PriceDetails(ValidatingObject, XmlObject, ComparableEqual):
    
    neededPriceTypes = [ 'net_customer' ]
    additionalPriceTypes = [ 'net_list' ]
   
    def __init__(self):
        self.validFrom = None
        self.validTo = None
        self.dailyPrice = None
        self.prices = []

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            pricesEqual = super().checkListForEquality(self.prices, other.prices)
            return pricesEqual and self.validFrom == other.validFrom and self.validTo == other.validTo and self.dailyPrice == other.dailyPrice
        
    def validate(self, raiseException=False):
        if self.prices is None or len(self.prices) == 0:
            logging.warning("Keine Preisangaben hinterlegt.")
        if not self.validFrom is None and not self.validTo is None and self.validFrom > self.validTo:
            logging.warning("Zeitspanne nicht gueltig.")
        if self.dailyPrice:
            super().logError("Tagespreis hinterlegt!", raiseException)
        pricenames = []
        for price in self.prices:
            price.validate(raiseException)
            if price.priceType in pricenames:
                self.logError("Jeder Preistyp darf nur einmal auftreten.s", raiseException)
    
        if not set(pricenames).issubset(PriceDetails.neededPriceTypes):
            self.logError("Mindestens ein Pflichtpreis ist nicht vorhanden: '{0}'".format(",".join(PriceDetails.neededPriceTypes)), raiseException)

    def addPrice(self, price):
        if price is not None:
            self.prices.append(price)

    def toXml(self):
        self.validate(True)
        priceDetailsXmlElement = Element("ARTICLE_PRICE_DETAILS")
        if self.validFrom is not None and self.validTo is not None:
            super().addDateTimeSubElement(priceDetailsXmlElement, "valid_start_date", self.validFrom)
            super().addDateTimeSubElement(priceDetailsXmlElement, "valid_end_date", self.validTo)
        super().addOptionalSubElement(priceDetailsXmlElement, "DAILY_PRICE", self.dailyPrice)
        super().addListOfSubElements(priceDetailsXmlElement, self.prices)
        return priceDetailsXmlElement