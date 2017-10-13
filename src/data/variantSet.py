'''
Created on 17.05.2017

@author: henrik.pilz
'''
from . import ValidatingXmlObject 
from lxml.etree import Element

class VariantSet(ValidatingXmlObject):
    def __init__(self):
        self.order = None
        self.variants = []

    def __eq__(self, other):
		if not super().__eq__(other):
			return False
		else:
			variantsEqual = super().checkListForEquality(self.variants, other.variants)                
			return variantsEqual and self.order == other.order
    
    def validate(self, raiseException=False):
        if self.order is None:
            super().logError("Die Reihenfolge der Suffixe ist nicht definitiert.", raiseException)
        if self.variants is None or len(self.variants)==0:
            super().logError("Keine Varianten fuer diesen Artikel vorhanden!", raiseException)
        else:
            for variant in self.variants:
                variant.validate(raiseException)

    def addVariant(self, variant):
        if variant not in self.variants:
            self.variants.append(variant)

    def __len__(self):
        return len(self.variants)
    
    def toXml(self):
        self.validate(True)
        xmlVariants = Element("VARIANTS")
        super().addMandatorySubElement(xmlVariants, "VORDER", self.order)
        for variant in self.variants:
            xmlVariants.append(variant.toXml())
        return xmlVariants        