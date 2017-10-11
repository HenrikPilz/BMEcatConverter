'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject


class Product(ValidatingXmlObject):

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
        if type(self) != type(other):
            return False

        priceDetailsEqual = super().checkListForEquality(self.priceDetails, other.priceDetails)
        mimeInfoEqual = super().checkListForEquality(self.mimeInfo, other.mimeInfo)        
        userDefinedExtensionsEqual = super().checkListForEquality(self.userDefinedExtensions, other.userDefinedExtensions)
        featureSetsEqual = super().checkListForEquality(self.featureSets, other.featureSets)
        referencesEqual = super().checkListForEquality(self.references, other.references)
        variantsEqualEqual = super().checkListForEquality(self.variants, other.variants)
                
        return priceDetailsEqual and mimeInfoEqual and userDefinedExtensionsEqual and featureSetsEqual and referencesEqual and variantsEqualEqual and self.productId == other.productId and self.details == other.details and self.orderDetails == other.orderDetails and self.hasVariants == other.hasVariants
    
    def __ne__(self, other):
        return not self.__eq__(other)
   
    def validate(self, raiseException=False):
        if self.productId is None:
            super().logError("Der Artikel hat keine Artikelnummer.", raiseException)
        if self.details is None:
            super().logError("Der Artikel hat keine Artikeldetails.", raiseException)
        else:
            self.details.validate(raiseException)
        if self.orderDetails is None:
            super().logError("Der Artikel hat keine Bestellinformation.", raiseException)
        else:
            self.orderDetails.validate(raiseException)
        if self.priceDetails is None or len(self.priceDetails) == 0:
            super().logError("Der Artikel hat keine Preisinformationen.", raiseException)
        else:
            for priceDetail in self.priceDetails:
                priceDetail.validate(raiseException)
            
        if self.mimeInfo is None or len(self.mimeInfo) == 0:
            logging.info("Es wurden keine Bilder gefunden.")
        else:
            for mime in self.mimeInfo:
                mime.validate(raiseException)
        if self.featureSets is None or len(self.featureSets) == 0:
            logging.info("Es wurden keine Attribute gefunden.")
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
        if len(featureSet) > 0:
            self.featureSets.append(featureSet)
        
            for feature in featureSet.features:
                if feature.variants is not None:
                    logging.info("Variante gefunden.")
                    self.__addVariant(feature)
        else:
            logging.info("Attributset ist leer und wird nicht gespeichert.")
    
    def __addVariant(self, feature):
        self.variants.append((feature.variants.order, feature.name, feature.variants))
        self.numberOfVariants *= len(feature.variants)
        self.hasVariants = len(feature.variants) > 0
    
