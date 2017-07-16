'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from data import ValidatingObject


class Mime(ValidatingObject):
    
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
        
    def validate(self, raiseException=False):
        if self.source is None:
            super().logError("Kein Bildpfad angegeben.", raiseException)
        if int(self.order) < 1:
            logging.info("Bildreihenfolge fehlerhaft: " + self.order)
        if not self.mimeType is None and self.mimeType not in Mime.__allowedTypes:
            logging.info("Bildtyp fehlerhaft: " + self.mimeType)
        if not self.purpose is None and self.purpose not in Mime.__allowedPurposes:
            logging.info("Bildverwendung fehlerhaft: " + self.purpose)
