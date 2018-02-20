'''
Created on 05.05.2017

@author: henrik.pilz
'''
import os

from datamodel.comparableEqual import ComparableEqual
from datamodel.validatingObject import FormulaFoundException
from datamodel.variantSet import VariantSet
from datamodel.xmlObject import ValidatingXMLObject
from mapping import UnitMapper


class Feature(ValidatingXMLObject, ComparableEqual):
    __baseDirectory = os.path.join(os.path.dirname(__file__), "..", "..", "documents", "BMEcat", "version")
    __bmecatUnitMapper = UnitMapper(os.path.join(__baseDirectory, "BMEcatUnitMapping.csv"))
    __etimUnitMapper = UnitMapper(os.path.join(__baseDirectory, "ETIMUnitMapping.csv"))
    __featureValueBlacklist = " -\n\t\r_\\/"

    def __init__(self):
        self.name = None
        self.order = None
        self.values = []
        self.variants = None
        self.unit = None
        self.description = None
        self.valueDetails = None

    def __len__(self):
        if self.variants is not None:
            return len(self.variants)
        else:
            return len(self.values)

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

    def _mapUnitIfNecessary(self):
        if self.unit is None:
            return
        self.unit = self.unit.strip()
        if self.__bmecatUnitMapper.hasKey(self.unit):
            self.unit = self.__bmecatUnitMapper.getSIUnit(self.unit)
        elif self.__etimUnitMapper.hasKey(self.unit):
            self.unit = self.__etimUnitMapper.getSIUnit(self.unit)

    def validate(self, raiseException=False):
        super().valueNotNoneOrEmpty(self.name, "Attibutename is missing.", raiseException)
        hasValues = super().valueNotNoneOrEmpty(self.values)
        hasVariants = super().valueNotNoneOrEmpty(self.variants)
        if not hasValues and not hasVariants:
            super().logError("Es wurden weder Attributswerte noch Varianten angegeben.", raiseException)
        elif hasValues and hasVariants:
            super().logError("Es wurden Attributswerte und Varianten angegeben. Die Zuordnung ist mehrdeutig.", raiseException)
        else:
            if hasVariants:
                self.variants.validate(raiseException)
        self._mapUnitIfNecessary()
        try:
            self.checkAttributesForFormulas(['name', 'order', 'unit', 'values'])
        except FormulaFoundException as ffe:
            raise FormulaFoundException("{0}: {1}".format(self.name, str(ffe)))

    def addValue(self, value):
        if value is not None and len(str(value).strip(self.__featureValueBlacklist)) > 0:
            self.add("values", value)

    def addVariantSet(self):
        if self.variants is None:
            self.variants = VariantSet()

    def addVariantOrder(self, order):
        self.addVariantSet()
        self.variants.order = order

    def addVariant(self, variant):
        self.addVariantSet()
        self.variants.addVariant(variant)

    def hasVariants(self):
        return self.variants is not None and len(self.variants) > 1

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
        else:
            xmlFeature.append(self.variants.toXml(raiseExceptionOnValidate))
        return xmlFeature
