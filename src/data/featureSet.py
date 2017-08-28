'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from data import ValidatingObject


class FeatureSet(ValidatingObject):
    def __init__(self):
        self.referenceSytem = None
        self.referenceGroupId = None
        self.features = []
        
    def addFeature(self,feature):
        try:
            feature.validate(True)
            self.features.append(feature)
        except Exception as ve:
            logging.info("Das Attribut enthaelt keine validen Werte. Es wird nicht hinzugefuegt. ", ve)
        
    def validate(self, raiseException=False):
        if self.features is None or len(self.features) == 0:
            logging.warning("Keine Attribute fuer diese Attributgruppe vorhanden!")
        else:
            for feature in self.features:
                feature.validate(raiseException)

    def __len__(self):
        return len(self.features)
