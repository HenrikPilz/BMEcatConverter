'''
Created on 17.05.2017

@author: henrik.pilz
'''
from data import ValidatingObject


class VariantSet(ValidatingObject):
    def __init__(self):
        self.order = None
        self.variants = []
        
    def validate(self, raiseException=False):
        if self.order is None:
            super().logError("Die Reihenfolge der Suffixe ist nicht definitiert.", raiseException)
        if self.variants is None or len(self.variants)==0:
            super().logError("Keine Varianten fuer diesen Artikel vorhanden!", raiseException)
        else:
            for variant in self.variants:
                variant.validate(raiseException)

    def addVariant(self, variant):
        self.variants.append(variant)

    def __len__(self):
        return len(self.variants)