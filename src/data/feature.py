'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

class Feature():
    def __init__(self):
        self.name = None
        self.values = []
        self.variants = None
        self.unit = None
        self.description = None
        self.valueDetails = None

    def validate(self):
        if self.name is None:
            logging.error("Der Merkmalsname fehlt.")
        if  self.values is not None and len(self.values) > 0 and self.variants is not None:
            logging.error("Es wurden Values und Varianten angegeben. Die Zuordnung ist mehrdeutig.")
        else:
            if self.variants is not None:
                self.variants.validate()
    
    def addValue(self, value):
        self.values.append(value)

    def addVariant(self, variant):
        self.variants.addVariant(variant)
        