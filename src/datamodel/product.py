'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

from lxml.etree import SubElement

from . import ValidatingXMLObject, ComparableEqual
from .orderDetails import OrderDetails
from .productDetails import ProductDetails


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

            return priceDetailsEqual and mimeInfoEqual and userDefinedExtensionsEqual and featureSetsEqual and \
                referencesEqual and variantsEqualEqual and productIdEqual and self.details == other.details and \
                self.orderDetails == other.orderDetails and self.hasVariants == other.hasVariants

    def __ne__(self, other):
        return not self.__eq__(other)

    def validate(self, raiseException=False):
        super().valueNotNone(self.productId, "Der Artikel hat keine Artikelnummer.", raiseException)
        messagePrefix = "Der Artikel '{0}' hat ".format(self.productId)
        super().valueNotNone(self.details, messagePrefix + "keine Artikeldetails.".format(self.productId), raiseException)
        try:
            self.details.validate(raiseException)
        except Exception as e:
            raise Exception(messagePrefix + "fehlerhafte Artikeldetails. " + str(e))
        super().valueNotNone(self.orderDetails, messagePrefix + "keine Bestellinformation.".format(self.productId), raiseException)
        try:
            self.orderDetails.validate(raiseException)
        except Exception as e:
            raise Exception(messagePrefix + "fehlerhafte Bestellinformationen. " + str(e))
        super().valueNotNoneOrEmpty(self.priceDetails, messagePrefix + "keine Preisinformationen.".format(self.productId), raiseException)
        super().validateList(self.priceDetails, messagePrefix + "fehlerhafte Preisinformationen.", raiseException)

        if super().valueNotNoneOrEmpty(self.mimeInfo, messagePrefix + "keine Bilder.".format(self.productId), False):
            super().validateList(self.mimeInfo, messagePrefix + "fehlerhafte Bildinformationen.", raiseException)

        if super().valueNotNoneOrEmpty(self.featureSets, messagePrefix + "keine Attribute.".format(self.productId), False):
            super().validateList(self.featureSets, messagePrefix + "fehlerhafte Attributinformationen.", raiseException)

    def addDetails(self):
        self.details = ProductDetails()

    def addOrderDetails(self):
        self.orderDetails = OrderDetails()

    def addPriceDetails(self, priceDetails, raiseException=True):
        self.addToListIfValid(priceDetails, self.priceDetails,
                              "Die Preisdetails enthalten keine validen Einträge. Sie werden nicht hinzugefuegt.", raiseException)

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

    def addReference(self, reference, raiseException=True):
        self.addToListIfValid(reference, self.references, "Die Referenz ist nicht valide. Sie wird nicht hinzugefügt.", raiseException)

    def addUserDefinedExtension(self, udf):
        '''self.userDefinedExtensions.append(udf)'''
        pass

    def addSpecialTreatmentClass(self, treatmentclass):
        self.details.addSpecialTreatmentClass(treatmentclass)

    def addKeyword(self, keyword):
        self.details.addKeyword(keyword)

    def addFeatureSet(self, featureSet):
        message = None
        if self.productId is not None:
            message = "Artikel '{0}' Attributset ist leer und wird nicht gespeichert.".format(self.productId)
        else:
            message = "Das Attributset ist leer und wird nicht gespeichert."
        if super().addToListIfValid(featureSet, self.featureSets, message):
            for feature in featureSet.features:
                if feature.hasVariants():
                    logging.info("Variante gefunden.")
                    self.__addVariant(feature)
        else:
            logging.debug(message)

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
        super().addListOfSubElements(articleElement, self.priceDetails, raiseExceptionOnValidate)
        if super().valueNotNoneOrEmpty(self.mimeInfo):
            mimeInfoElement = SubElement(articleElement, "MIME_INFO")
            super().addListOfSubElements(mimeInfoElement, sorted(self.mimeInfo, key=lambda mime: int(mime.order)), raiseExceptionOnValidate)
        super().addListOfSubElements(articleElement, self.featureSets, raiseExceptionOnValidate)
        super().addListOfSubElements(articleElement, self.references, raiseExceptionOnValidate)
        return articleElement
