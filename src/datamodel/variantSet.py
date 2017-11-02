'''
Created on 17.05.2017

@author: henrik.pilz
'''
from . import ValidatingXMLObject, ComparableEqual 


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
        if self.order is None:
            super().logError("Die Reihenfolge der Suffixe ist nicht definitiert.", raiseException)
        if self.variants is None or len(self.variants)==0:
            super().logError("Keine Varianten fuer diesen Artikel vorhanden!", raiseException)
        else:
            for variant in self.variants:
                variant.validate(raiseException)

    def addVariant(self, variant):
        super().addToListIfValid(variant, self.variants, "Keine Variante hinzugefügt.")

    def __len__(self):
        return len(self.variants)
    
    def toXml(self, raiseExceptionOnValidate=True):
        xmlVariants = super().validateAndCreateBaseElement("VARIANTS", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(xmlVariants, "VORDER", self.order)
        super().addListOfSubElements(xmlVariants, self.variants, raiseExceptionOnValidate)
        return xmlVariants