'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

from datamodel.comparableEqual import ComparableEqual
from datamodel.xmlObject import ValidatingXMLObject


class Price(ValidatingXMLObject, ComparableEqual):

    def __init__(self, priceType=None):
        self.priceType = priceType
        self.amount = None
        self.currency = "EUR"
        self.tax = 0.19
        self.lowerBound = 1
        self.factor = None
        self.territory = None

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            amountNone = self.amount is None and other.amount is None
            amountNotNone = self.amount is not None and other.amount is not None
            amountEqual = amountNone or (amountNotNone and float(self.amount) == float(other.amount))
            taxEqual = float(self.tax) == float(other.tax)
            lowerBoundEqual = int(self.lowerBound) == int(other.lowerBound)
            factorNone = self.factor is None and other.factor is None
            factorNotNone = self.factor is not None and other.factor is not None
            factorEqual = factorNone or (factorNotNone and float(self.factor) == float(other.factor))
            currencyEqual = str(self.currency) == str(other.currency)
            return self.priceType == other.priceType and amountEqual and currencyEqual and taxEqual and lowerBoundEqual and factorEqual

    def validate(self, raiseException=False):
        if self.valueNotNone(self.amount, "Kein Preis angegeben!", raiseException) and float(self.amount) < 0:
            self.amount = 0
            super().logError("Negativer Preis angegeben!", raiseException)
        if self.priceType is None:
            logging.warning("Kein Typ fuer den Preis angeben!")
        if float(self.tax) not in [ 0.19, 0.07 ]:
            logging.warning("Ungueltige Steuerangabe: {t:f}. Steuer auf 0.19 gesetzt.".format(t=self.tax))
            self.tax = 0.19
        if self.currency != "EUR":
            logging.warning("Waehrung nicht in EURO: " + str(self.currency))
        if float(self.lowerBound) < 1:
            logging.warning("Staffelmenge falsch!")

    def toXml(self, raiseExceptionOnValidate=True):
        priceXmlElement = super().validateAndCreateBaseElement("ARTICLE_PRICE", { "price_type" : self.priceType }, raiseExceptionOnValidate)
        super().addMandatorySubElement(priceXmlElement, "PRICE_AMOUNT", self.amount)
        super().addMandatorySubElement(priceXmlElement, "PRICE_CURRENCY", self.currency)
        super().addMandatorySubElement(priceXmlElement, "TAX", self.tax)
        super().addMandatorySubElement(priceXmlElement, "LOWER_BOUND", self.lowerBound)

        super().addOptionalSubElement(priceXmlElement, "PRICE_FACTOR", self.factor)
        super().addOptionalSubElement(priceXmlElement, "TERRITORY", self.territory)

        return priceXmlElement
