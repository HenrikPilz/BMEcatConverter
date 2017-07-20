'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from data import ValidatingObject


class Reference(ValidatingObject):
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
