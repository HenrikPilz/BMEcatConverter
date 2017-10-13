'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject


class Mime(ValidatingXmlObject):
    
    __allowedTypes = [ "url", "application/pdf", "image/jpeg", "image/jpg", "image/tif", "text/html", "text/plain" ]
    __allowedPurposes = [ "thumbnail", "normal", "detail", "data_sheet", "logo", "others" ]
    __allowedCombinations = {}
    
    def __init__(self):
        self.source = None
        self.mimeType = None
        self.description = None
        self.altenativeContent = None
        self.purpose = None
        self.order = 1
        
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            return self.source == other.source and self.mimeType == other.mimeType and self.description == other.description and self.altenativeContent == other.altenativeContent and self.purpose == other.purpose and self.order == other.order
        
    def validate(self, raiseException=False):
        if self.source is None:
            super().logError("Kein Bildpfad angegeben.", raiseException)
        if int(self.order) < 1:
            logging.info("Bildreihenfolge fehlerhaft: " + str(self.order))
        if not self.mimeType is None and self.mimeType not in Mime.__allowedTypes:
            logging.info("Bildtyp fehlerhaft: " + str(self.mimeType))
        if not self.purpose is None and self.purpose not in Mime.__allowedPurposes:
            logging.info("Bildverwendung fehlerhaft: " + str(self.purpose))
