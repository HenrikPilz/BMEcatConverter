'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

from lxml.etree import SubElement

from . import ValidatingXMLObject, ComparableEqual


class Product(ValidatingXMLObject, ComparableEqual):

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
        super().valueNotNone(self.productId, "Der Artikel hat keine Artikelnummer.", raiseException)
        super().valueNotNone(self.details, "Der Artikel '{0}' hat keine Artikeldetails.".format(self.productId), raiseException)
        self.details.validate(raiseException)
        super().valueNotNone(self.orderDetails, "Der Artikel '{0}' hat keine Bestellinformation.".format(self.productId), raiseException)
        self.orderDetails.validate(raiseException)
        super().valueNotNoneOrEmpty(self.priceDetails, "Der Artikel '{0}' hat keine Preisinformationen.".format(self.productId), raiseException)
        super().validateList(self.priceDetails, raiseException)
            
        if super().valueNotNoneOrEmpty(self.mimeInfo, "Für Artikel '{0}' wurden keine Bilder gefunden.".format(self.productId), False):
            super().validateList(self.mimeInfo, raiseException)

        if super().valueNotNoneOrEmpty(self.featureSets, "Für Artikel '{0}' wurden keine Attribute gefunden.".format(self.productId), False):
            super().validateList(self.featureSets, raiseException)

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
        
    def addMime(self, mime, raiseException=True):
        self.addToListIfValid(mime, self.mimeInfo, "Das Bild enthaelt keine validen Einträge. Es wird nicht hinzugefuegt.", raiseException)

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
        # Anzahl bestehender Varianter multipliziert mit der Anzahl definierter Varianter in diesem Feature
        self.numberOfVariants *= len(feature.variants)
        self.hasVariants = self.numberOfVariants > 1
    
    def toXml(self, articleType='new', raiseExceptionOnValidate=True):
        articleElement = super().validateAndCreateBaseElement("ARTICLE", { "mode" : articleType }, raiseExceptionOnValidate)
        super().addMandatorySubElement(articleElement, "SUPPLIER_AID", self.productId)
        articleElement.append(self.details.toXml(raiseExceptionOnValidate))
        articleElement.append(self.orderDetails.toXml(raiseExceptionOnValidate))
        super().addListOfSubElements(articleElement, self.priceDetails)
        mimeInfoElement = SubElement(articleElement, "MIME_INFO")        
        super().addListOfSubElements(mimeInfoElement, sorted(self.mimeInfo, key=lambda mime: int(mime.order)), raiseExceptionOnValidate)
        super().addListOfSubElements(articleElement, self.featureSets, raiseExceptionOnValidate)
        super().addListOfSubElements(articleElement, self.references, raiseExceptionOnValidate)        
        return articleElement