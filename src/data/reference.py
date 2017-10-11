'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject


class Reference(ValidatingXmlObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.referenceType = None
        self.supplierArticleIds = []
        self.quantity = 1
        self.description = None
        self.mimeInfo = []

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        supplierArticleIdsEqual = super().checkListForEquality(self.supplierArticleIds, other.supplierArticleIds)
        mimeInfoEqual = super().checkListForEquality(self.mimeInfo, other.mimeInfo)
        
        return supplierArticleIdsEqual and mimeInfoEqual and self.referenceType == other.referenceType and self.quantity == other.quantity

    def validate(self,  raiseException=False):
        if self.referenceType is None:
            super().logError("Der Referenz wurde kein Typ zugewiesen.",  raiseException)
        if self.supplierArticleIds is None or len(self.supplierArticleIds) == 0:
            super().logError("Es wird keine Artikelnummer referenziert.",  raiseException)
        if int(self.quantity) != len(self.supplierArticleIds):
            logging.warning("Anzahl referenzierter Artikel stimmt nicht mit der Anzahl der vorhandenen Artikelnummern ueberein..")
        if self.mimeInfo is None or len(self.mimeInfo) == 0:
            logging.info("Es wurden keine Bilder gefunden.")
        else:
            for mime in self.mimeInfo:
                mime.validate(raiseException)

    def addMime(self, mime):
        self.mimeInfo.append(mime)
        
    def addSupplierArticleId(self, supplierArticleId):
        self.supplierArticleIds.append(supplierArticleId)
