'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject


class ProductDetails(ValidatingXmlObject):
    
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

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            # Folgende Dinge werden erstmal vernachlässigt.        
            # specialTreatmentClassesEqual
            # keywordsEqual
            # remarksEqual
            # segmentEqual
            # self.manufacturerTypeDescription == other.manufacturerTypeDescription
            # self.erpGroupBuyer == other.erpGroupBuyer
            # self.erpGroupSupplier == other.erpGroupSupplier
            # self.supplierAltId == other.supplierAltId
            # self.buyerId == other.buyerId
            # self.articleOrder == other.articleOrder
            # self.articleStatus == other.articleStatus
        
            return self.title == other.title and self.description == other.description and self.ean == other.ean and self.manufacturerArticleId == other.manufacturerArticleId and self.manufacturerName == self.manufacturerName and self.deliveryTime == other.deliveryTime

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