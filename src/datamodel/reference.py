'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

from datamodel.comparableEqual import ComparableEqual
from datamodel.xmlObject import ValidatingXMLObject


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

    def validate(self, raiseException=False):
        self.valueNotNone(self.referenceType, "Der Referenz wurde kein Typ zugewiesen.", raiseException)
        self.valueNotNone(self.supplierArticleId, "Es wird keine Artikelnummer referenziert.", raiseException)
        if self.quantity is not None and self.referenceType != "constists_of":
            logging.warning("Die Anzahl sollte nur gesetzt werden, falls der type 'constists_of' ist.")
            self.quantity = None

        super().validateIfNotNoneOrEmpty(self.mimeInfo,
                                         None,
                                         "Die Referenz hat fehlerhafte Bildinformationen.",
                                         raiseException)

    def addMime(self, mime):
        super().addToListIfValid(mime, self.mimeInfo, "Bilddaten für Referenz fehlerhaft", False)

    def addSupplierArticleId(self, supplierArticleId):
        if self.supplierArticleId == supplierArticleId:
            return
        if self.supplierArticleId is not None:
            raise Exception("Es wird schon eine Artikelnummer referenziert: {0}".format(self.supplierArticleId))
        self.supplierArticleId = supplierArticleId

    def toXml(self, raiseExceptionOnValidate=True):
        attributes = { "type" : self.referenceType }
        if self.quantity is not None:
            attributes["quantity"] = str(int(self.quantity))
        referenceElement = super().validateAndCreateBaseElement("ARTICLE_REFERENCE", attributes, raiseExceptionOnValidate)
        super().addMandatorySubElement(referenceElement, "ART_ID_TO", self.supplierArticleId)
        super().addOptionalSubElement(referenceElement, "CATALOG_ID", self.catalogId)
        super().addOptionalSubElement(referenceElement, "CATALOG_VERSION", self.catalogVersion)
        return referenceElement
