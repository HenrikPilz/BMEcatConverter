'''
Created on 05.05.2017

@author: henrik.pilz
'''
from data import ValidatingObject
from data.variantSet import VariantSet

class Feature(ValidatingObject):
    def __init__(self):
        self.name = None
        self.values = []
        self.variants = None
        self.unit = None
        self.description = None
        self.valueDetails = None

    def validate(self, raiseException=False):
        errMsg = None
        if self.name is None or len(self.name.strip()) == 0:
            errMsg = "Der Merkmalsname fehlt."
            super().logError(errMsg, raiseException)
                
        if (self.values is None or len(self.values) == 0) and (self.variants is None or len(self.variants) == 0):
            errMsg = "Es wurden weder Attributswerte noch Varianten angegeben."
            super().logError(errMsg, raiseException)
        elif len(self.values) > 0 and self.variants is not None and len(self.variants) > 0:
            errMsg = "Es wurden Values und Varianten angegeben. Die Zuordnung ist mehrdeutig."
            super().logError(errMsg, raiseException)
        else:
            if self.variants is not None:
                self.variants.validate()
    
    def addValue(self, value):
        if value is not None:
            if type(value) is str and len(value.strip()) > 0:
                self.values.append(value)
            elif type(value) is not str: 
                self.values.append(value)
            else:
                pass

    def addVariantOrder(self, order):
        if self.variants is None:
            self.variants = VariantSet()
        self.variants.order = order

    def addVariant(self, variant):
        if self.variants is None:
            self.variants = VariantSet()
        self.variants.addVariant(variant)
        