'''
Created on 05.05.2017

@author: henrik.pilz
'''
from . import ValidatingXmlObject
from .variantSet import VariantSet
from lxml.etree import Element

class Feature(ValidatingXmlObject):
    def __init__(self):
        self.name = None
        self.order = None
        self.values = []
        self.variants = None
        self.unit = None
        self.description = None
        self.valueDetails = None

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            valuesEqual = super().checkListForEquality(self.values, other.values)
            return valuesEqual and self.name == other.name and self.variants == other.variants and self.unit == other.unit and self.description == other.description and self.valueDetails == other.valueDetails
    
    def validate(self, raiseException=False):
        errMsg = None
        super().valueNotNoneOrEmpty(self.name, "Der Merkmalsname fehlt.", raiseException)
        hasValues = super().valueNotNoneOrEmpty(self.values, "Keine Attributswerte", False)
        hasVariants = super().valueNotNoneOrEmpty(self.variants, "Keine Varianten", False)
        if not hasValues and not hasVariants:
            errMsg = "Es wurden weder Attributswerte noch Varianten angegeben."
            super().logError(errMsg, raiseException)
        elif hasValues and hasVariants:
            errMsg = "Es wurden Values und Varianten angegeben. Die Zuordnung ist mehrdeutig."
            super().logError(errMsg, raiseException)
        else:
            if hasVariants:
                self.variants.validate(raiseException)
                    
    
    def addValue(self, value):
        """
        Validiert, ob der übergebene Wert nicht leer ist und fügt ihn zur Liste der Values hinzu, falls das der Fall ist.  
        """
        valueNotEmpty = super().valueNotNoneOrEmpty(value, "Kein Wert übergeben.", False)
        if valueNotEmpty and value not in self.values:
            if type(value) is str: 
                self.values.append(value)
            else: 
                self.values.append(value)

    def addVariantOrder(self, order):
        if self.variants is None:
            self.variants = VariantSet()
        self.variants.order = order

    def addVariant(self, variant):
        if self.variants is None:
            self.variants = VariantSet()
        self.variants.addVariant(variant)
    

    def toXml(self):
        self.validate(True)
        xmlFeature = Element("FEATURE")
        super().addMandatorySubElement(xmlFeature, "FNAME", self.name)
        super().addOptionalSubElement(xmlFeature, "FORDER", self.order)
        super().addOptionalSubElement(xmlFeature, "FUNIT", self.unit)
        super().addOptionalSubElement(xmlFeature, "FDESCR", self.description)
        super().addOptionalSubElement(xmlFeature, "FVALUE_DETAILS", self.valueDetails)

        if len(self.values) > 0:
            for value in self.values:
                super().addMandatorySubElement(xmlFeature, "FVALUE", value)
        if self.variants is not None:
            xmlFeature.append(self.variants.toXml())