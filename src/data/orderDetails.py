'''
Created on 05.05.2017

@author: henrik.pilz
'''

import logging


class OrderDetails():
    allowedOrderUnits = [ "C62", "MTR", "SET", "BX", "CT", "PF", "BG", "PK", "TN", "DR", "CA", "CS", "RO" ]
    allowedContentUnits = [ "C62", "MTR", "SET", "RO", "DR", "CS", "PR", "RO" ]
    __allowedCombinations = {}

    def __init__(self):
        self.orderUnit = "C62"
        self.contentUnit = "C62"
        self.packingQuantity = 1
        self.priceQuantity = 1
        self.quantityMin = 1
        self.quantityInterval = 1        

    def validate(self):
        if self.orderUnit is None or self.orderUnit.strip() == "":
            raise Exception("Keine Bestelleinheit angeben.")
        if self.contentUnit is None or self.orderUnit.strip() == "":
            raise Exception("Keine Verpackungseinheit angeben.")
        if self.orderUnit not in OrderDetails.allowedOrderUnits:
            logging.warning("Falsche Bestelleinheit angeben: " + self.orderUnit)
        if self.contentUnit not in OrderDetails.allowedContentUnits:
            logging.warning("Falsche Verpackungseinheit angeben: " + self.contentUnit)
        if float(self.quantityMin) != float(self.quantityInterval):
            logging.info("Mindestbestellmenge und Bestellintervall sollten gleich sein.")
        if float(self.packingQuantity) > 1 and float(self.quantityMin) > 1:
            logging.warning("Mindestbestellmenge und PackingQuantity duerfen nicht beide ungleich eins sein.")
        if float(self.quantityMin) != float(self.priceQuantity):
            logging.info("PackagingQuantity und PriceQuantity untscheiden sich!")
