'''
Created on 05.05.2017

@author: henrik.pilz
'''

import logging

from datamodel.validatingObject import ComparableEqual
from datamodel.validatingObject import ValidatingXMLObject


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
        super().valueNotEmptyOrNoneAndNotIn(self.orderUnit, "Keine Bestelleinheit angeben.",
                                            self.__allowedOrderUnits, "Falsche Bestelleinheit angeben.", raiseException)
        super().valueNotEmptyOrNoneAndNotIn(self.contentUnit, "Keine Verpackungseinheit angeben.",
                                            self.__allowedContentUnits, "Falsche Verpackungseinheit angeben.", raiseException)

        if float(self.quantityMin) != float(self.quantityInterval):
            super().logError("Mindestbestellmenge und Bestellintervall sollten gleich sein.", raiseException)
        if float(self.packingQuantity) > 1 and float(self.quantityMin) > 1:
            # super().logError("Mindestbestellmenge und PackingQuantity duerfen nicht beide ungleich eins sein.", raiseException)
            logging.warning("Mindestbestellmenge und PackingQuantity duerfen nicht beide ungleich eins sein.")
        if float(self.quantityMin) != float(self.priceQuantity):
            logging.info("PackagingQuantity und PriceQuantity untscheiden sich!")

    def toXml(self, raiseExceptionOnValidate=True):
        orderDetailsXmlElement = super().validateAndCreateBaseElement("ARTICLE_ORDER_DETAILS", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(orderDetailsXmlElement, "ORDER_UNIT", self.orderUnit)
        super().addMandatorySubElement(orderDetailsXmlElement, "CONTENT_UNIT", self.contentUnit)
        super().addMandatorySubElement(orderDetailsXmlElement, "NO_CU_PER_OU", self.packingQuantity)
        super().addMandatorySubElement(orderDetailsXmlElement, "QUANTITY_MIN", self.quantityMin)
        super().addMandatorySubElement(orderDetailsXmlElement, "QUANTITY_INTERVAL", self.quantityInterval)
        super().addMandatorySubElement(orderDetailsXmlElement, "PRICE_QUANTITY", self.priceQuantity)
        return orderDetailsXmlElement
