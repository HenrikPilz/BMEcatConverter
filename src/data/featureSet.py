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
        
    def validate(self):
        if self.features is None or len(self.features)==0:
            logging.warning("Keine Attribute für diese Attributgruppe vorhanden!")
        else:
            for feature in self.features:
                feature.validate()
