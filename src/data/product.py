'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging


class Product():

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
   
    def validate(self):
        if self.productId is None:
            logging.error("Der Artikel hat keine Artikelnummer.")
        if self.details is None:
            logging.error("Der Artikel hat Artikeldetails.")
        else:
            self.details.validate()
        if self.orderDetails is None:
            logging.error("Der Artikel hat Bestellinformation.")
        else:
            self.orderDetails.validate()
        if self.priceDetails is None or len(self.priceDetails) == 0:
            logging.error("Der Artikel hat keine Preisinformationen.")
        else:
            for priceDetail in self.priceDetails:
                priceDetail.validate()
            
        if self.mimeInfo is None or len(self.mimeInfo) == 0:
            logging.info("Es wurden keine Bilder gefunden.")
        else:
            for mime in self.mimeInfo:
                mime.validate()
        if self.featureSets is None or len(self.featureSets) == 0:
            logging.info("Es wurden keine Attribute gefunden.")
        else:
            for featureSet in self.featureSets:
                featureSet.validate()
                for feature in featureSet.features:
                    if feature.variants is not None and len(feature.variants) > 0:
                        self.hasVariants = True

    def addPriceDetails(self, priceDetails):
        self.priceDetails.append(priceDetails)
        
    def addTitle(self, title):
        self.details.title = title

    def addDescription(self, description):
        self.details.description = description

    def addManufacturerId(self, manufacturerId):
        self.details.manufacturerId = manufacturerId

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
    