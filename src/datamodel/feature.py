'''
Created on 05.05.2017

@author: henrik.pilz
'''
from . import ValidatingXMLObject, ComparableEqual
from .variantSet import VariantSet

class Feature(ValidatingXMLObject, ComparableEqual):
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
            namesEqual = self.name == other.name
            valuesEqual = super().checkListForEquality([str(value) for value in self.values], [str(value) for value in other.values])
            unitsEqual = self.unit == other.unit
            bothHaveVariants = super().valueNotNoneOrEmpty(self.variants) and super().valueNotNoneOrEmpty(other.variants)
            noVariantsAtAll = self.variants is None and other.variants is None
            variantsAreEqual = True
            if bothHaveVariants:
                variantsAreEqual = self.variants == other.variants
            else:
                variantsAreEqual = noVariantsAtAll
            return namesEqual and unitsEqual and valuesEqual and variantsAreEqual
    
    def validate(self, raiseException=False):
        errMsg = None
        super().valueNotNoneOrEmpty(self.name, "Der Merkmalsname fehlt.", raiseException)
        hasValues = super().valueNotNoneOrEmpty(self.values)
        hasVariants = super().valueNotNoneOrEmpty(self.variants)
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
    
    def toXml(self, raiseExceptionOnValidate=True):
        xmlFeature = super().validateAndCreateBaseElement("FEATURE", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(xmlFeature, "FNAME", self.name)
        super().addOptionalSubElement(xmlFeature, "FORDER", self.order)
        super().addOptionalSubElement(xmlFeature, "FUNIT", self.unit)
        super().addOptionalSubElement(xmlFeature, "FDESCR", self.description)
        super().addOptionalSubElement(xmlFeature, "FVALUE_DETAILS", self.valueDetails)

        if len(self.values) > 0:
            for value in self.values:
                super().addMandatorySubElement(xmlFeature, "FVALUE", value)
        if self.variants is not None:
            xmlFeature.append(self.variants.toXml(raiseExceptionOnValidate))
        return xmlFeature