'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from data import ValidatingObject


class PriceDetails(ValidatingObject):
   
    def __init__(self):
        self.validFrom = None
        self.validTo = None
        self.dailyPrice = False
        self.prices = []
        
    def validate(self, raiseException=False):
        if self.prices is None or len(self.prices) == 0:
            logging.warning("Keine Preisangaben hinterlegt.")
        if not self.validFrom is None and not self.validTo is None and self.validFrom > self.validTo:
            logging.warning("Zeitspanne nicht gueltig.")
        if self.dailyPrice:
            super().logError("Tagespreis hinterlegt!", raiseException)
        for price in self.prices:
            price.validate(raiseException)
    
    def addPrice(self, price):
        if price is not None:
            self.prices.append(price)