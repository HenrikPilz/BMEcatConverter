'''
Created on 05.05.2017

@author: henrik.pilz
'''

import logging
from . import ValidatingXmlObject


class OrderDetails(ValidatingXmlObject):
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

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return self.orderUnit == other.orderUnit and self.contentUnit == other.contentUnit and self.packingQuantity == other.packingQuantity and self.priceQuantity == other.priceQuantity and self.quantityMin == other.quantityMin and self.quantityInterval == other.quantityInterval

    def validate(self, raiseException=False):
        if self.orderUnit is None or self.orderUnit.strip() == "":
            super().logError("Keine Bestelleinheit angeben.", raiseException)
        if self.orderUnit not in OrderDetails.allowedOrderUnits:
            super().logError("Falsche Bestelleinheit angeben: " + str(self.orderUnit), raiseException)
        if self.contentUnit is None or self.contentUnit.strip() == "":
            super().logError("Keine Verpackungseinheit angeben.", raiseException)
        if self.contentUnit not in OrderDetails.allowedContentUnits:
            super().logError("Falsche Verpackungseinheit angeben: " + str(self.contentUnit), raiseException)
        if float(self.quantityMin) != float(self.quantityInterval):
            logging.info("Mindestbestellmenge und Bestellintervall sollten gleich sein.")
        if float(self.packingQuantity) > 1 and float(self.quantityMin) > 1:
            logging.warning("Mindestbestellmenge und PackingQuantity duerfen nicht beide ungleich eins sein.")
        if float(self.quantityMin) != float(self.priceQuantity):
            logging.info("PackagingQuantity und PriceQuantity untscheiden sich!")
