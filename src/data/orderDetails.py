'''
Created on 05.05.2017

@author: henrik.pilz
'''

import logging
from . import ValidatingXmlObject
from lxml.etree import Element


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
        if not super().__eq__(other):
            return False
        else:
            priceQuantityEqual = int(self.priceQuantity) == int(other.priceQuantity)
            quantityMinEqual = int(self.quantityMin) == int(other.quantityMin)
            quantityIntervalEqual = int(self.quantityInterval) == int(other.quantityInterval)
            packingQuantityEqual = int(self.packingQuantity) == int(other.packingQuantity)
            return self.orderUnit == other.orderUnit and self.contentUnit == other.contentUnit and packingQuantityEqual and priceQuantityEqual and quantityMinEqual and quantityIntervalEqual

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

    def toXml(self):
        self.validate(True)
        orderDetailsXmlElement = Element("ARTICLE_ORDER_DETAILS")
        super().addMandatorySubElement(orderDetailsXmlElement, "ORDER_UNIT", self.orderUnit)
        super().addMandatorySubElement(orderDetailsXmlElement, "CONTENT_UNIT", self.contentUnit)
        super().addMandatorySubElement(orderDetailsXmlElement, "NO_CU_PER_OU", self.packingQuantity)
        super().addMandatorySubElement(orderDetailsXmlElement, "QUANTITY_MIN", self.quantityMin)
        super().addMandatorySubElement(orderDetailsXmlElement, "QUANTITY_INTERVAL", self.quantityInterval)
        super().addMandatorySubElement(orderDetailsXmlElement, "PRICE_QUANTITY", self.priceQuantity)
        return orderDetailsXmlElement