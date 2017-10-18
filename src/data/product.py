'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingObject, XmlObject, ComparableEqual
from lxml.etree import Element, SubElement


class Product(ValidatingObject, XmlObject, ComparableEqual):

    def __init__(self):        
        self.productId = None
        self.details = None
        self.orderDetails = None
        self.priceDetails = []
        self.mimeInfo = []
        self.userDefinedExtensions = {}
        self.featureSets = []
        self.references = []
        self.hasVariants = False
        self.variants = []
        self.numberOfVariants = 1

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            priceDetailsEqual = super().checkListForEquality(self.priceDetails, other.priceDetails)
            mimeInfoEqual = super().checkListForEquality(self.mimeInfo, other.mimeInfo)        
            userDefinedExtensionsEqual = super().checkListForEquality(self.userDefinedExtensions, other.userDefinedExtensions)
            featureSetsEqual = super().checkListForEquality(self.featureSets, other.featureSets)
            referencesEqual = super().checkListForEquality(self.references, other.references)
            variantsEqualEqual = super().checkListForEquality(self.variants, other.variants)
            productIdEqual = str(self.productId) == str(other.productId)
                    
            return priceDetailsEqual and mimeInfoEqual and userDefinedExtensionsEqual and featureSetsEqual and referencesEqual and variantsEqualEqual and productIdEqual and self.details == other.details and self.orderDetails == other.orderDetails and self.hasVariants == other.hasVariants
    
    def __ne__(self, other):
        return not self.__eq__(other)
   
    def validate(self, raiseException=False):
        if self.productId is None:
            super().logError("Der Artikel hat keine Artikelnummer.", raiseException)
        if self.details is None:
            super().logError("Der Artikel '{0}' hat keine Artikeldetails.".format(self.productId), raiseException)
        else:
            self.details.validate(raiseException)
        if self.orderDetails is None:
            super().logError("Der Artikel '{0}' hat keine Bestellinformation.".format(self.productId), raiseException)
        else:
            self.orderDetails.validate(raiseException)
        if self.priceDetails is None or len(self.priceDetails) == 0:
            super().logError("Der Artikel '{0}' hat keine Preisinformationen.".format(self.productId), raiseException)
        else:
            for priceDetail in self.priceDetails:
                priceDetail.validate(raiseException)
            
        if self.mimeInfo is None or len(self.mimeInfo) == 0:
            logging.info("Für Artikel '{0}' wurden keine Bilder gefunden.".format(self.productId))
        else:
            for mime in self.mimeInfo:
                mime.validate(raiseException)
        if self.featureSets is None or len(self.featureSets) == 0:
            logging.info("Für Artikel '{0}' wurden keine Attribute gefunden.".format(self.productId))
        else:
            for featureSet in self.featureSets:
                featureSet.validate(raiseException)
                for feature in featureSet.features:
                    if feature.variants is not None and len(feature.variants) > 0:
                        self.hasVariants = True

    def addPriceDetails(self, priceDetails):
        self.priceDetails.append(priceDetails)
        
    def addTitle(self, title):
        self.details.title = title

    def addDescription(self, description):
        self.details.description = description

    def addManufacturerArticleId(self, manufacturerArticleId):
        self.details.manufacturerArticleId = manufacturerArticleId

    def addManufacturerName(self, manufacturerName):
        self.details.manufacturerName = manufacturerName

    def addEAN(self, ean):
        self.details.ean = ean
    
    def addDeliveryTime(self, deliveryTime):
        self.details.deliveryTime = deliveryTime
        
    def addMime(self, mime):
        self.mimeInfo.append(mime)

    def addReference(self, reference):
        self.references.append(reference)

    def addUserDefinedExtension(self, udf):
        '''self.userDefinedExtensions.append(udf)'''
        pass
        
    def addSpecialTreatmentClass(self, treatmentclass):
        self.details.addSpecialTreatmentClass(treatmentclass)
        
    def addKeyword(self, keyword):
        self.details.addKeyword(keyword)

    def addFeatureSet(self, featureSet):
        if len(featureSet) > 0 and featureSet not in self.featureSets:
            self.featureSets.append(featureSet)
        
            for feature in featureSet.features:
                if feature.variants is not None:
                    logging.info("Variante gefunden.")
                    self.__addVariant(feature)
        else:
            message = None
            if self.productId is not None:
                message = "Artikel '{0}' Attributset ist leer und wird nicht gespeichert.".format(self.productId)
            else:
                message = "Das Attributset ist leer und wird nicht gespeichert."
            logging.info(message)
    
    def __addVariant(self, feature):
        self.variants.append((feature.variants.order, feature.name, feature.variants))
        self.numberOfVariants *= len(feature.variants)
        self.hasVariants = len(feature.variants) > 0
    
    def toXml(self, articleType='new'):
        self.validate(True)
        articleElement = Element("ARTICLE", { "mode" : articleType })
        super().addMandatorySubElement(articleElement, "SUPPLIER_AID", self.productId)
        articleElement.append(self.details.toXml())
        articleElement.append(self.orderDetails.toXml())
        super().addListOfSubElements(articleElement, self.priceDetails)
        mimeInfoElement = SubElement(articleElement, "MIME_INFO")
        super().addListOfSubElements(mimeInfoElement, self.mimeInfo)
        super().addListOfSubElements(articleElement, self.featureSets)
        super().addListOfSubElements(articleElement, self.references)        
        return articleElement

    def __checkUpdateAndSortMimes(self):
        raise Exception("FEHLT")