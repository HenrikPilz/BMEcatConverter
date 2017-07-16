'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging


class PriceDetails():
   
    def __init__(self):
        self.validFrom = None
        self.validTo = None
        self.dailyPrice = False
        self.prices = []
        
    def validate(self):
        if self.prices is None or len(self.prices) == 0:
            logging.warning("Keine Preisangaben hinterlegt.")
        if not self.validFrom is None and not self.validTo is None and self.validFrom > self.validTo:
            logging.warning("Zeitspanne nicht gueltig.")
        if self.dailyPrice:
            logging.error("Tagespreis hinterlegt!")
        for price in self.prices:
            price.validate()
    
    def addPrice(self, price):
        if not price is None:
            self.prices.append(price)

