'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

class ProductDetails():
    
    def __init__(self):
        self.title = None
        self.description = None
        self.manufacturerTypeDescription = None
        ''' Mapping !!'''
        self.ean = None
        self.supplierAltId = None
        self.buyerId = None
        self.manufacturerId = None
        self.manufacturerName = None
        self.erpGroupBuyer = None
        self.erpGroupSupplier = None
        self.deliveryTime = 2
        self.specialTreatmentClasses = []
        self.keyword = {}
        self.remarks = []
        self.segment = []
        self.articleOrder = 1
        self.articleStatus = None        

    def validate(self):
        if self.title is None or self.title.strip() == "":
            logging.error("Ein Artikelname fehlt")
        if self.description is None or self.description.strip() == "":
            logging.warning("Die Artikelbeschreibung fehlt.")
        if self.ean is None or self.ean.strip() == "":
            logging.warning("Keine EAN vorhanden.")
    
    def addSpecialTreatmentClass(self, treatmentclass):
        self.specialTreatmentClasses.append(treatmentclass)