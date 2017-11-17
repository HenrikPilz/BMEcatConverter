'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXMLObject, ComparableEqual

class ProductDetails(ValidatingXMLObject, ComparableEqual):
    
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
            eanNone = self.ean is None and other.ean is None
            eanNotNone = self.ean is not None and other.ean is not None
            eanEqual = eanNone or (eanNotNone and int(self.ean) == int(other.ean))
            manufacturerArticleIdEqual = str(self.manufacturerArticleId) == str(other.manufacturerArticleId)
            deliveryTimeEqual = float(self.deliveryTime) == float(other.deliveryTime)
            return self.title == other.title and self.description == other.description and eanEqual and manufacturerArticleIdEqual and self.manufacturerName == other.manufacturerName and deliveryTimeEqual

    def validate(self, raiseException=False):
        if self.title is None or self.title.strip() == "":
            super().logError("Ein Artikelname fehlt", raiseException)
        if self.description is None or self.description.strip() == "":
            logging.warning("Die Artikelbeschreibung fehlt.")
        if self.ean is None or (isinstance(self.ean, str) and self.ean.strip() == ""):
            logging.warning("Keine EAN vorhanden.")
    
    def addSpecialTreatmentClass(self, treatmentclass):
        self.specialTreatmentClasses.append(treatmentclass)
    
    def addKeyword(self, keyword):
        if super().valueNotNoneOrEmpty(keyword):
            self.keywords.append(keyword)
    
    def toXml(self, raiseExceptionOnValidate=True):
        detailsXmlElement = super().validateAndCreateBaseElement("ARTICLE_DETAILS", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(detailsXmlElement, "DESCRIPTION_SHORT", self.title)
        
        super().addOptionalSubElement(detailsXmlElement, "DESCRIPTION_LONG", self.description)
        super().addOptionalSubElement(detailsXmlElement, "EAN", self.ean)
        super().addOptionalSubElement(detailsXmlElement, "MANUFACTURER_AID", self.manufacturerArticleId)
        super().addOptionalSubElement(detailsXmlElement, "MANUFACTURER_NAME", self.manufacturerName)
        
        super().addOptionalSubElement(detailsXmlElement, "SUPPLIER_ALT_AID", self.supplierAltId)
        super().addOptionalSubElement(detailsXmlElement, "BUYER_AID ", self.buyerId)
        super().addOptionalSubElement(detailsXmlElement, "ERP_GROUP_BUYER", self.erpGroupBuyer)
        super().addOptionalSubElement(detailsXmlElement, "ERP_GROUP_SUPPLIER", self.erpGroupSupplier)
        super().addOptionalSubElement(detailsXmlElement, "ARTICLE_STATUS", self.articleStatus)
        super().addOptionalSubElement(detailsXmlElement, "ARTICLE_ORDER", self.articleOrder)

        super().addMandatorySubElement(detailsXmlElement, "DELIVERY_TIME", self.deliveryTime)
        
        for keyword in self.keywords:
            super().addOptionalSubElement(detailsXmlElement,"KEYWORD", keyword)
        
        super().addListOfSubElements(detailsXmlElement, self.specialTreatmentClasses, raiseExceptionOnValidate)
        return detailsXmlElement