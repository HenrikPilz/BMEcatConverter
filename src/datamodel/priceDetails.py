'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXMLObject, ComparableEqual


class PriceDetails(ValidatingXMLObject, ComparableEqual):

    mandatoryPriceTypes = [ 'net_customer' ]
    optionalPriceTypes = [ 'net_list' ]

    def __init__(self):
        self.validFrom = None
        self.validTo = None
        self.dailyPrice = None
        self.prices = []

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            pricesEqual = super().checkListForEquality(self.prices, other.prices)
            return pricesEqual and self.validFrom == other.validFrom and self.validTo == other.validTo and self.dailyPrice == other.dailyPrice

    def __len__(self):
        return len(self.prices)

    def validate(self, raiseException=False):
        super().valueNotNoneOrEmpty(self.prices, "Keine Preisangaben hinterlegt.", raiseException)

        if self.validFrom is not None and self.validTo is not None and self.validFrom > self.validTo:
            logging.warning("Zeitspanne nicht gueltig.")
        if self.dailyPrice:
            super().logError("Tagespreis hinterlegt!", raiseException)
        pricenames = []
        for price in self.prices:
            price.validate(raiseException)
            if price.priceType in pricenames:
                self.logError("Jeder Preistyp darf nur einmal auftreten. Doppelt: '{0}'".format(price.priceType), raiseException)
            else:
                pricenames.append(price.priceType)

        atLeastOneOfTheMandatoryPricesIsMissing = not set(self.mandatoryPriceTypes).issubset(pricenames)
        if len(pricenames) == 0 or atLeastOneOfTheMandatoryPricesIsMissing:
            missingPriceTypes = ",".join(set(self.mandatoryPriceTypes).difference(pricenames))
            self.logError("Mindestens ein Pflichtpreis ist nicht vorhanden: '{0}'".format(missingPriceTypes), raiseException)

    def addPrice(self, price, raiseException=True):
        self.addToListIfValid(price, self.prices, "Der Preis enthaelt keine validen Einträge. Er wird nicht hinzugefuegt.", raiseException=raiseException)

    def toXml(self, raiseExceptionOnValidate=True):
        priceDetailsXmlElement = super().validateAndCreateBaseElement("ARTICLE_PRICE_DETAILS", raiseExceptionOnValidate=raiseExceptionOnValidate)
        if self.validFrom is not None and self.validTo is not None:
            super().addDateTimeSubElement(priceDetailsXmlElement, "valid_start_date", self.validFrom)
            super().addDateTimeSubElement(priceDetailsXmlElement, "valid_end_date", self.validTo)
        super().addOptionalSubElement(priceDetailsXmlElement, "DAILY_PRICE", self.dailyPrice)
        super().addListOfSubElements(priceDetailsXmlElement, self.prices, raiseExceptionOnValidate)
        return priceDetailsXmlElement
