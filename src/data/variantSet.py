'''
Created on 17.05.2017

@author: henrik.pilz
'''
import logging

class VariantSet():
    def __init__(self):
        self.order = None
        self.variants = []
        
    def validate(self):
        if self.order is None:
            logging.error("Die Reihenfolge der Suffixe ist nicht definitiert.")
        if self.variants is None or len(self.variants)==0:
            logging.warning("Keine Varianten für diesen Artikel vorhanden!")
        else:
            for variant in self.variants:
                variant.validate()

    def addVariant(self, variant):
        self.variants.append(variant)

    def __len__(self):
        return len(self.variants)