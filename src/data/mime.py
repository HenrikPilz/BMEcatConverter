'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

class Mime():
    
    allowedTypes = [ "url", "application/pdf", "image/jpeg", "image/jpg", "image/tif", "text/html", "text/plain" ]
    allowedPurposes = [ "thumbnail", "normal", "detail", "data_sheet", "logo", "others" ]
    allowedCombinations = {}
    
    def __init__(self):
        self.source = None
        self.mimeType = None
        self.description = None
        self.altenativeContent = None
        self.purpose = None
        self.order = 1
        
    def validate(self):
        if self.source is None:
            logging.error("Kein Bildpfad angegeben.")
        if int(self.order) < 1:
            logging.info("Bildreihenfolge fehlerhaft: " + self.order)
        if not self.mimeType is None and self.mimeType not in Mime.allowedTypes:
            logging.info("Bildtyp fehlerhaft: " + self.mimeType)
        if not self.purpose is None and self.purpose not in Mime.allowedPurposes:
            logging.info("Bildverwendung fehlerhaft: " + self.purpose)
