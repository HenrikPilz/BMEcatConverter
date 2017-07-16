'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging


class Reference(object):
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

    def validate(self):
        if self.referenceType is None:
            raise Exception("Der Referenz wurde kein Typ zugewiesen.")
        if self.supplierArticleIds is None or len(self.supplierArticleIds) == 0:
            logging.error("Es wird keine Artikelnummer referenziert.")
        if int(self.quantity) != len(self.supplierArticleIds):
            logging.warning("Anzahl referenzierter Artikel stimmt nicht mit der Anzahl der vorhandenen Artikelnummern ueberein..")
        if self.mimeInfo is None or len(self.mimeInfo) == 0:
            logging.info("Es wurden keine Bilder gefunden.")
        else:
            for mime in self.mimeInfo:
                mime.validate()

    def addMime(self, mime):
        self.mimeInfo.append(mime)
