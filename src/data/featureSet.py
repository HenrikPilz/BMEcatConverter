'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

class FeatureSet():
    def __init__(self):
        self.referenceSytem = None
        self.referenceGroupId = None
        self.features = []
        
    def addFeature(self,feature):
        try:
            feature.validate(True)
            self.features.append(feature)
        except Exception as ve:
            logging.info("Das Attribut enthält keine validen Werte. Es wird nicht hinzugefügt. ", ve)
        
    def validate(self):
        if self.features is None or len(self.features)==0:
            logging.warning("Keine Attribute für diese Attributgruppe vorhanden!")
        else:
            for feature in self.features:
                feature.validate()

    def __len__(self):
        return len(self.features)