'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingObject, XmlObject, ComparableEqual
from lxml.etree import Element

class Price(ValidatingObject, XmlObject, ComparableEqual):
    
    def __init__(self):
        self.priceType = None
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
            amountEqual = float(self.amount) == float(other.amount)
            taxEqual = float(self.tax) == float(other.tax)
            lowerBoundEqual = int(self.lowerBound) == int(other.lowerBound)
            factorEqual = float(self.factor) == float(other.factor)
            return self.priceType == other.priceType and amountEqual and self.currency == other.currency and taxEqual and lowerBoundEqual and factorEqual and self.territory == other.territory

    def validate(self, raiseException=False):
        if self.amount is None:
            super().logError("Kein Preis angegeben!", raiseException)
        elif float(self.amount) < 0:
            self.amount = 0
            super().logError("Negativer Preis angegeben!", raiseException)
        if self.priceType is None:
            logging.warning("Kein Typ fuer den Preis angeben!")
        if float(self.tax) not in  [ 0.19, 0.07 ]:
            logging.warning("Ungueltige Steuerangabe: {t:f}. Steuer auf 0.19 gesetzt.".format(t=self.tax))
            self.tax = 0.19
        if self.currency != "EUR":
            logging.warning("Waehrung nicht in EURO: " + str(self.currency))
        if float(self.lowerBound) < 1:
            logging.warning("Staffelmenge falsch!")
            
    def toXml(self):
        self.validate(True)
        priceXmlElement = Element("ARTICLE_PRICE", { "price_type" : self.priceType })
        super().addMandatorySubElement(priceXmlElement, "PRICE_AMOUNT", self.amount)
        super().addMandatorySubElement(priceXmlElement, "PRICE_CURRENCY", self.currency)
        super().addMandatorySubElement(priceXmlElement, "TAX", self.tax)
        super().addMandatorySubElement(priceXmlElement, "LOWER_BOUND", self.lowerBound)
        
        super().addOptionalSubElement(priceXmlElement, "PRICE_FACTOR", self.factor)
        super().addOptionalSubElement(priceXmlElement, "TERRITORY", self.territory)
        
        return priceXmlElement