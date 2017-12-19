'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
import os

from lxml.etree import SubElement

from datamodel.orderDetails import OrderDetails
from datamodel.productDetails import ProductDetails
from datamodel.validatingObject import ComparableEqual
from datamodel.validatingObject import ValidatingXMLObject
from mapping.blacklist import Blacklist


class Product(ValidatingXMLObject, ComparableEqual):

    __baseDirectory = os.path.join(os.path.dirname(__file__), "..", "..", "documents", "BMEcat", "version")
    __featureSetBlacklist = Blacklist(os.path.join(__baseDirectory, "FeatureSetBlacklist.csv"))

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
            featureSetsEqual = super().checkListForEquality(self.featureSets, other.featureSets)
            productIdEqual = str(self.productId) == str(other.productId)
            # Varianten werden ueber Featuresets verglichen.
            # Referenzen sind hierbei unwichtig.
            # User Defined Extensions sind noch nicht implementiert.
            # userDefinedExtensionsEqual = super().checkListForEquality(self.userDefinedExtensions, other.userDefinedExtensions)

            return productIdEqual and self.details == other.details and self.orderDetails == other.orderDetails and \
                priceDetailsEqual and mimeInfoEqual and featureSetsEqual

    def validate(self, raiseException=False):
        super().valueNotNone(self.productId, "Der Artikel hat keine Artikelnummer.", raiseException)
        self.productId = str(self.productId).strip()
        messagePrefix = "Der Artikel '{0}' hat ".format(self.productId)
        super().valueNotNone(self.details, messagePrefix + "keine Artikeldetails.", raiseException)
        self._tryValidatingSubElement(self.details, messagePrefix + "fehlerhafte Artikeldetails.", raiseException)
        super().valueNotNone(self.orderDetails, messagePrefix + "keine Bestellinformation.", raiseException)
        self._tryValidatingSubElement(self.orderDetails, messagePrefix + "fehlerhafte Bestellinformationen.", raiseException)
        super().valueNotNoneOrEmpty(self.priceDetails, messagePrefix + "keine Preisinformationen.", raiseException)
        super().validateList(self.priceDetails, messagePrefix + "fehlerhafte Preisinformationen.", raiseException)

        self._validateIfNotNoneOrEmpty(self.mimeInfo,
                                       messagePrefix + "keine Bilder.",
                                       messagePrefix + "fehlerhafte Bildinformationen.",
                                       raiseException)

        self._validateIfNotNoneOrEmpty(self.featureSets,
                                       messagePrefix + "keine Attribute.",
                                       messagePrefix + "fehlerhafte Attributinformationen.",
                                       raiseException)

    def _validateIfNotNoneOrEmpty(self, elementToCheck, noneOrEmptyMessage, validationMessage, raiseException=False):
        if super().valueNotNoneOrEmpty(elementToCheck, noneOrEmptyMessage, False):
            super().validateList(elementToCheck, validationMessage, raiseException)

    def _tryValidatingSubElement(self, subElement, exceptionMessage, raiseException=True):
        try:
            subElement.validate(raiseException)
        except Exception as e:
            raise Exception(exceptionMessage + " " + str(e))

    def addDetails(self):
        if self.details is None:
            self.details = ProductDetails()

    def addOrderDetails(self):
        if self.orderDetails is None:
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
        if self.__featureSetBlacklist.contains(featureSet.referenceSystem):
            logging.info("Attributset wird nicht gespeichert, da es auf der Blacklist ist.")
            return

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
