'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from data import ValidatingObject


class ProductDetails(ValidatingObject):
    
    def __init__(self):
        self.title = None
        self.description = None
        self.manufacturerTypeDescription = None
        ''' Mapping !!'''
        self.ean = None
        self.supplierAltId = None
        self.buyerId = None
        self.manufacturerArticleId = None
        self.manufacturerName = None
        self.erpGroupBuyer = None
        self.erpGroupSupplier = None
        self.deliveryTime = 2
        self.specialTreatmentClasses = []
        self.keywords = []
        self.remarks = []
        self.segment = []
        self.articleOrder = 1
        self.articleStatus = None        

    def validate(self, raiseException=False):
        if self.title is None or self.title.strip() == "":
            super().logError("Ein Artikelname fehlt", raiseException)
        if self.description is None or self.description.strip() == "":
            logging.warning("Die Artikelbeschreibung fehlt.")
        if self.ean is None or self.ean.strip() == "":
            logging.warning("Keine EAN vorhanden.")
    
    def addSpecialTreatmentClass(self, treatmentclass):
        self.specialTreatmentClasses.append(treatmentclass)
    
    def addKeyword(self, keyword):
        self.keywords.append(keyword)