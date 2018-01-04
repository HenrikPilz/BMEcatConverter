'''
Created on 17.05.2017

@author: henrik.pilz
'''
from datamodel.comparableEqual import ComparableEqual
from datamodel.xmlObject import ValidatingXMLObject


class VariantSet(ValidatingXMLObject, ComparableEqual):
    def __init__(self):
        self.order = None
        self.variants = []

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            return super().checkListForEquality(self.variants, other.variants)

    def validate(self, raiseException=False):
        super().valueNotNone(self.order, "Die Reihenfolge der Suffixe ist nicht definitiert.", raiseException)
        super().validateIfNotNoneOrEmptyRaiseException(self.variants,
                                                       "Keine Varianten fuer diesen Artikel vorhanden!",
                                                       "Fehlerhafte Varianten fuer diesen Artikel vorhanden!",
                                                       raiseException)

    def addVariant(self, variant):
        super().addToListIfValid(variant, self.variants, "Keine Variante hinzugefügt.")

    def __len__(self):
        return len(self.variants)

    def toXml(self, raiseExceptionOnValidate=True):
        xmlVariants = super().validateAndCreateBaseElement("VARIANTS", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(xmlVariants, "VORDER", self.order)
        super().addListOfSubElements(xmlVariants, self.variants, raiseExceptionOnValidate)
        return xmlVariants
