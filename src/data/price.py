'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject

class Price(ValidatingXmlObject):
    
    def __init__(self):
        self.priceType = None
        self.amount = None
        self.currency = "EUR"
        self.tax = 0.19
        self.lowerBound = 1
        self.factor = 1.0
        self.territory = "DEU"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.priceType == other.priceType and self.amount == other.amount and self.currency == other.currency and self.tax == other.tax and self.lowerBound == other.lowerBound and self.factor == other.factor and self.territory == other.territory

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