'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

class Price():
    
    def __init__(self):
        self.priceType = None
        self.amount = None
        self.currency = "EUR"
        self.tax = 0.19
        self.lowerBound = 1
        self.factor = 1.0
        self.territory = "DEU"

    def validate(self):
        if self.amount is None:
            logging.error("Kein Preis angegeben!")
        elif float(self.amount) < 0:
            logging.error("Negativer Preis angegeben!")
        if self.priceType is None:
            logging.warning("Kein Typ für den Preis angeben!")
        if float(self.tax) not in  [ 0.19, 0.07 ]:
            logging.warning("Ungültige Steuerangabe: {t:f}".format(t=self.tax))
        if self.currency != "EUR":
            logging.warning("Währung nicht in EURO: " + self.currency)
        if float(self.lowerBound) < 1:
            logging.warning("Staffelmenge falsch!")