'''
Created on 05.05.2017

@author: henrik.pilz
'''

import logging

from . import ValidatingXMLObject, ComparableEqual


class OrderDetails(ValidatingXMLObject, ComparableEqual):
    __allowedOrderUnits = [ "C62", "MTR", "SET", "BX", "CT", "PF", "BG", "PK", "TN", "DR", "CA", "CS", "RO" ]
    __allowedContentUnits = [ "C62", "MTR", "SET", "RO", "DR", "CS", "PR", "RO" ]
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
            orderUnitEqual = self.orderUnit == other.orderUnit
            contentUnitEqual = self.contentUnit == other.contentUnit
            unitsEqual = orderUnitEqual and contentUnitEqual
            orderUnitValuesEqual = quantityIntervalEqual and quantityMinEqual
            return unitsEqual and orderUnitValuesEqual and priceQuantityEqual and packingQuantityEqual

    def validate(self, raiseException=False):
        if super().valueNotNoneOrEmpty(self.orderUnit, "Keine Bestelleinheit angeben.", raiseException) and self.orderUnit not in OrderDetails.__allowedOrderUnits:
            super().logError("Falsche Bestelleinheit angeben: " + str(self.orderUnit), raiseException)
        if super().valueNotNoneOrEmpty(self.contentUnit,"Keine Verpackungseinheit angeben.", raiseException) and self.contentUnit not in OrderDetails.__allowedContentUnits:
            super().logError("Falsche Verpackungseinheit angeben: " + str(self.contentUnit), raiseException)
        if float(self.quantityMin) != float(self.quantityInterval):
            logging.info("Mindestbestellmenge und Bestellintervall sollten gleich sein.")
        if float(self.packingQuantity) > 1 and float(self.quantityMin) > 1:
            logging.warning("Mindestbestellmenge und PackingQuantity duerfen nicht beide ungleich eins sein.")
        if float(self.quantityMin) != float(self.priceQuantity):
            logging.info("PackagingQuantity und PriceQuantity untscheiden sich!")

    def toXml(self):
        orderDetailsXmlElement = super().validateAndCreateBaseElement("ARTICLE_ORDER_DETAILS")
        super().addMandatorySubElement(orderDetailsXmlElement, "ORDER_UNIT", self.orderUnit)
        super().addMandatorySubElement(orderDetailsXmlElement, "CONTENT_UNIT", self.contentUnit)
        super().addMandatorySubElement(orderDetailsXmlElement, "NO_CU_PER_OU", self.packingQuantity)
        super().addMandatorySubElement(orderDetailsXmlElement, "QUANTITY_MIN", self.quantityMin)
        super().addMandatorySubElement(orderDetailsXmlElement, "QUANTITY_INTERVAL", self.quantityInterval)
        super().addMandatorySubElement(orderDetailsXmlElement, "PRICE_QUANTITY", self.priceQuantity)
        return orderDetailsXmlElement