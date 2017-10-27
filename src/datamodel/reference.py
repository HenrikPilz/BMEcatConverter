'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXMLObject, ComparableEqual

class Reference(ValidatingXMLObject, ComparableEqual):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.referenceType = None
        self.supplierArticleId = None
        self.supplierId = None
        self.quantity = None
        self.catalogId = None
        self.catalogVersion = None
        self.description = None
        self.mimeInfo = []

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            supplierArticleIdEqual = str(self.supplierArticleId) == str(other.supplierArticleId)
            mimeInfoEqual = super().checkListForEquality(self.mimeInfo, other.mimeInfo)
        
            return supplierArticleIdEqual and mimeInfoEqual and self.referenceType == other.referenceType and str(self.quantity) == str(other.quantity)


    def validate(self,  raiseException=False):
        if self.referenceType is None:
            super().logError("Der Referenz wurde kein Typ zugewiesen.",  raiseException)
        if self.supplierArticleId is None:
            super().logError("Es wird keine Artikelnummer referenziert.",  raiseException)
        if self.quantity is not None and self.referenceType != "constists_of":
            logging.warning("Anzahl ist kein Attribute, welches gesetzt werden darf.")
            self.quantity = None
        if self.mimeInfo is None or len(self.mimeInfo) == 0:
            logging.info("Es wurden keine Bilder gefunden.")
        else:
            for mime in self.mimeInfo:
                mime.validate(raiseException)


    def addMime(self, mime):
        self.mimeInfo.append(mime)
        
    def addSupplierArticleId(self, supplierArticleId):
        if self.supplierArticleId is not None:
            raise Exception("Es wird schon eine Artikelnummer referenziert: {0}".format(self.supplierArticleId))
        self.supplierArticleId = supplierArticleId 
    
    def toXml(self):
        attributes = { "type" : self.referenceType }
        if self.quantity is not None:
            attributes["quantity"] = self.quantity
        referenceElement = super().validateAndCreateBaseElement("ARTICLE_REFERENCE", attributes)
        super().addMandatorySubElement(referenceElement, "ART_ID_TO", self.supplierArticleId)
        super().addOptionalSubElement(referenceElement, "CATALOG_ID", self.catalogId)
        super().addOptionalSubElement(referenceElement, "CATALOG_VERSION", self.catalogVersion)
        return referenceElement
        
