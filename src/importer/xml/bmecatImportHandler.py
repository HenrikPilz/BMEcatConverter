'''
Created on 05.05.2017

@author: henrik.pilz
'''
from array import array
from datetime import datetime
from xml.sax import handler
import logging

from datamodel import Feature
from datamodel import FeatureSet
from datamodel import Mime
from datamodel import Price
from datamodel import PriceDetails
from datamodel import Product
from datamodel import Reference
from datamodel import TreatmentClass
from datamodel import ValidatingObject
from datamodel import Variant
from transformer import SeparatorTransformer


class BMEcatImportHandler(handler.ContentHandler):
    '''
        Handler fuer Sax2Parser, welcher BMEcats in den Formaten 1.01,1.2,2005, 2005.1 sowie ETIM aller Arten liest.
    '''

    ''' alle registrierten StartElementhandler '''
    __startElementHandler = { "article" : "createProduct",
                              "article_details" : "createProductDetails",
                              "order_details" : "createOrderDetails",
                              "price_details" : "createPriceDetails",
                              "price" : "createPrice",
                              "mime" : "createMime",
                              "mime_info" : "startMimeInfo",
                              "datetime" : "startDateTime",
                              "article_features" : "createFeatureSet",
                              "feature" : "createFeature",
                              "special_treatment_class" : "createTreatmentClass",
                              "article_reference" : "createReference",
                              "variants" : "createFeatureVariantSet",
                              "variant" : "createFeatureVariant",
                              "description_long" : "_startDescription",
                              "description" : "_startDescription" }

    ''' Moegliche Aliase fuer Varianten der BMEcats '''
    __alias = {
                "product" : "article",
                "product_details" : "article_details",
                "supplier_pid" : "supplier_aid",
                "supplier_alt_pid" : "supplier_alt_aid",
                "manufacturer_pid" : "manufacturer_aid",
                "buyer_pid" : "buyer_aid",
                "article_order_details" : "order_details",
                "article_price_details" : "price_details",
                "article_price" : "price",
                "product_features" : "article_features",
                "international_pid" : "ean",
                "product_order_details" : "order_details",
                "product_price_details" : "price_details",
                "product_price" : "price",
                "product_reference" : "article_reference",
                "prod_id_to" : "art_id_to",
                "supplier_pid_supplement" : "supplier_aid_supplement"
            }

    ''' alle registrierten EndElementhandler '''
    __endElementHandler = {
                "catalog_group_system" : "_resetAll",
                "feature" : "saveFeature",
                "article" : "saveProduct",
                "mime" : "saveMime",
                "variants" : "saveFeatureVariantSet",
                "vorder" : "addFeatureVariantSetOrder",
                "variant" : "addFeatureVariant",
                "article_features" : "saveFeatureSet",
                "special_treatment_class" : "saveTreatmentClass",
                "article_reference" : "saveReference",
                "price" : "savePrice",
                "price_details" : "savePriceDetails",
                "mime_info" : "endMimeInfo",
                "datetime" : "endDateTime",
                "article_details" : "endProductDetails",
                "order_details" : "endOrderDetails",
                "date" : "addDate",
                # Informationen am CurrentElement
                "territory" : ("_addAttributeToCurrentElement", "territory", False),
                "keyword" : ("_addAttributeToCurrentElement", "keywords", False),
                # Artikelinformationen
                "supplier_aid" : ("_addAttributeToCurrentArticle", "productId", True),
                "supplier_alt_aid" : ("_addAttributeToCurrentArticleDetails", "supplierAltId", False),
                "buyer_aid" : ("_addAttributeToCurrentArticleDetails", "buyerId", False),
                "manufacturer_aid" : ("_addAttributeToCurrentArticleDetails", "manufacturerArticleId", False),
                "manufacturer_name" : ("_addAttributeToCurrentArticleDetails", "manufacturerName", False),
                "ean" : ("_addAttributeToCurrentArticleDetails", "ean", False),
                "description_long" : ("_addAttributeToCurrentArticleDetails", "description", False),
                "description_short" : ("_addAttributeToCurrentArticleDetails", "title", False),
                "delivery_time" : ("_addAttributeToCurrentArticleDetails", "deliveryTime", False),
                "article_status" : ("_addAttributeToCurrentArticleDetails", "articleStatus", False),
                # Preisinformationen
                "price_amount" : ("_addAttributeToCurrentPrice", "amount", False),
                "tax" : ("_addAttributeToCurrentPrice", "tax", False),
                "price_currency" : ("_addAttributeToCurrentPrice", "currency", False),
                "price_factor" : ("_addAttributeToCurrentPrice", "factor", False),
                "lower_bound" : ("_addAttributeToCurrentPrice", "lowerBound", False),
                # Bestellinformationen
                "order_unit" : ("_addAttributeToCurrentArticleOrderDetails", "orderUnit", False),
                "content_unit" : ("_addAttributeToCurrentArticleOrderDetails", "contentUnit", False),
                "no_cu_per_ou" : ("_addAttributeToCurrentArticleOrderDetails", "packingQuantity", False),
                "price_quantity" : ("_addAttributeToCurrentArticleOrderDetails", "priceQuantity", False),
                "quantity_min" : ("_addAttributeToCurrentArticleOrderDetails", "quantityMin", False),
                "quantity_interval" : ("_addAttributeToCurrentArticleOrderDetails", "quantityInterval", False),
                # Bildinformationen
                "mime_source" : ("_addAttributeToCurrentMime", "source", False),
                "mime_type" : ("_addAttributeToCurrentMime", "mimeType", False),
                "mime_descr" : ("_addAttributeToCurrentMime", "description", False),
                "mime_alt" : ("_addAttributeToCurrentMime", "alternativeContent", False),
                "mime_purpose" : ("_addAttributeToCurrentMime", "purpose", False),
                "mime_order" : ("_addAttributeToCurrentMime", "order", False),
                # Attributinformationen
                "fname" : ("_addAttributeToCurrentFeature", "name", False),
                "fvalue" : ("_addAttributeToCurrentFeature", "values", False),
                "fvalue_details" : ("_addAttributeToCurrentFeature", "valueDetails", False),
                "funit" : ("_addAttributeToCurrentFeature", "unit", False),
                "fdesc" : ("_addAttributeToCurrentFeature", "description", False),
                # Referenzinformationen
                "art_id_to" : ("_addAttributeToCurrentReference", "supplierArticleId", False),
                "reference_descr" : ("_addAttributeToCurrentReference", "description", False),
                # AttributeSetinformationen
                "supplier_aid_supplement" : ("_addAttributeToCurrentVariant", "productIdSuffix", False),
                "reference_feature_system_name" : ("_addAttributeToCurrentFeatureSet", "referenceSystem", False),
                "reference_feature_group_id" : ("_addAttributeToCurrentFeatureSet", "referenceGroupId", False),
                "reference_feature_group_name" : ("_addAttributeToCurrentFeatureSet", "referenceGroupName", False) }

    __fieldsToTransform = [ "amount", "tax", "factor"]

    ''' Konstruktor '''
    def __init__(self, dateFormat, separatorTransformer=SeparatorTransformer("detect")):
        self.__dateFormat = dateFormat
        self._separatorTransformer = separatorTransformer

        '''articles by SKU and Product Structure as Value'''
        self.articles = { "new" : [], "update" : [], "delete" : [], "failed" : [] }
        self.__currentArticle = None
        self.__currentPrice = None
        self.__currentMime = None
        self.__currentArticleDetails = None
        self.__currentOrderDetails = None
        self.__currentPriceDetails = None
        self.__currentElement = None
        self.__currentContent = ""
        self.__dateType = None
        self.__currentFeatureSet = None
        self.__currentFeature = None
        self.__currentTreatmentClass = None
        self.__currentReference = None
        self.__currentVariant = None
        self.__currentVariantSet = None
        self.__lineFeedToHTML = False
        self.__currentArticleMode = "failed"

    ''' Starte aktuelles XML Element '''
    def startElement(self, name, attrs):
        self._workOnElement(name, attrs, True)

    ''' Schliesse aktuelles XML Element '''
    def endElement(self, name):
        self._workOnElement(name, None, False)

    ''' Handler ermitteln, der die Arbeit macht. '''
    def _workOnElement(self, name, attrs, bOpen):
        logging.debug("Call for Tag <" + name + ">")
        method = None
        try:
            handlerInfo = self._determineTagHandlername(name, bOpen)
            if handlerInfo is None:
                self.__currentContent = ""
                return

            if isinstance(handlerInfo, (tuple)):
                method = getattr(self, handlerInfo[0])
                method(handlerInfo[1], handlerInfo[2])
            else:
                method = getattr(self, handlerInfo)
                method(attrs)
            self.__currentContent = ""
        except AttributeError:
            raise NotImplementedError("Class [{0}] does not implement [{1}]".format(self.__class__.__name__, method))

    ''' Handlernamen fuer das XML-Element ermitteln. '''
    def _determineTagName(self, tag, bOpen):
        name = tag.lower()
        if tag.lower() in self.__alias:
            logging.debug("[{0}] '{1}' has an alias".format("start" if bOpen else "end", tag))
            name = self.__alias[tag.lower()]
        return name

    def _determineTagHandlername(self, tag, bOpen):
        name = self._determineTagName(tag, bOpen)
        if bOpen:
            return self._determineHandlername(name, self.__startElementHandler)
        else:
            return self._determineHandlername(name, self.__endElementHandler)

    def _determineHandlername(self, name, handlerByName):
            try:
                return handlerByName[name]
            except KeyError:
                logging.debug("Call for Tag <" + name + "> FAILED:")

    ''' ---------------------------------------------------------------------'''
    def _resetAll(self, attrs=None):
        self.__currentArticle = None
        self.__currentPrice = None
        self.__currentMime = None
        self.__currentPriceDetails = None
        self.__currentElement = None
        self.__currentContent = ""
        self.__dateType = None
        self.__currentFeatureSet = None
        self.__currentFeature = None
        self.__currentTreatmentClass = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Artikel '''
    def createProduct(self, attrs):
        logging.debug("Anfang Produkt " + ", ".join(attrs.getNames()))
        self._objectIsNotNone(self.__currentArticle,
                              "Fehler im BMEcat: Neuer Artikel soll erstellt werden. Es wird schon ein Artikel verarbeitet.",
                              True)
        self.__currentArticle = Product()
        self.__currentContent = ""
        self.__currentElement = self.__currentArticle
        if 'mode' in attrs.getNames():
            self.__currentArticleMode = attrs.getValue('mode')
        else:
            self.__currentArticleMode = 'new'
            logging.warning("Fehler im BMEcat: es wurde kein mode fuer den Artikel angegeben.")

    ''' Artikel speichern '''
    def saveProduct(self, attr=None):
        logging.info("Produkt validieren: " + self.__currentArticle.productId)
        self._objectIsNone(self.__currentArticle , "Es wurde kein aktuell zu bearbeitender Artikel gefunden.", True)
        self.__currentArticle.validate(False)
        logging.debug("Neues Produkt erstellt. Modus: " + self.__currentArticleMode)
        self.articles[self.__currentArticleMode].append(self.__currentArticle)
        logging.debug("Produktende")
        self._resetAll()

    ''' ---------------------------------------------------------------------'''
    def createProductDetails(self, attrs):
        self._objectIsNone(self.__currentArticle,
                           "Artikeldetails sollen erstellt werden. Aber es ist kein Artikel vorhanden", True)
        self._objectIsNotNone(self.__currentArticle.details,
                              "Fehler im BMEcat: Neue Artikeldetails sollen erstellt werden. Es werden schon Artikeldetails verarbeitet.", True)
        self.__currentArticle.addDetails()
        self.__currentArticleDetails = self.__currentArticle.details
        self.__currentElement = self.__currentArticle.details

    def endProductDetails(self, attrs=None):
        self.__currentArticleDetails = None
        self.__currentElement = self.__currentArticle

    ''' ---------------------------------------------------------------------'''
    def createOrderDetails(self, attrs=None):
        self._objectIsNone(self.__currentArticle,
                           "Bestelldetails sollen erstellt werden. Aber es ist kein Artikel vorhanden", True)
        self._objectIsNotNone(self.__currentOrderDetails,
                              "Fehler im BMEcat: Neue Bestelldetails sollen erstellt werden. Es werden schon Bestelldetails verarbeitet.", True)
        self.__currentArticle.addOrderDetails()
        self.__currentOrderDetails = self.__currentArticle.orderDetails

    def endOrderDetails(self, attrs=None):
        self._objectIsNone(self.__currentArticle,
                           "Bestelldetails sollen gespeichert werden. Aber es ist kein Artikel vorhanden", True)
        self.__currentOrderDetails = None
        self.__currentElement = self.__currentArticle

    ''' ---------------------------------------------------------------------'''
    def createPriceDetails(self, attrs):
        self._objectIsNotNone(self.__currentPriceDetails,
                              "Fehler im BMEcat: Neue Preisdetails sollen erstellt werden. Es werden schon Preisdetails verarbeitet.", True)
        self.__currentPriceDetails = PriceDetails()
        self.__currentElement = self.__currentPriceDetails

    def savePriceDetails(self, attrs):
        self._objectIsNone(self.__currentArticle,
                           "Preisdetails sollen gespeichert werden. Aber es ist kein Artikel vorhanden", True)
        self.__currentArticle.addPriceDetails(self.__currentPriceDetails, False)
        self.__currentPriceDetails = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Preis '''
    def createPrice(self, attrs):
        self._objectIsNotNone(self.__currentPrice,
                              "Fehler im BMEcat: Neuer Preis soll erstellt werden. Es wird schon ein Preis verarbeitet.", True)
        self.__currentPrice = Price(attrs.getValue('price_type'))
        self.__currentElement = self.__currentPrice

    ''' Preis speichern '''
    def savePrice(self, attrs):
        self._objectIsNone(self.__currentPriceDetails, "Preis soll gespeichert werden. Aber es sind keine Preisdetails  vorhanden", True)
        self.__currentPriceDetails.addPrice(self.__currentPrice, False)
        self.__currentPrice = None
        self.__currentElement = self.__currentPriceDetails

    ''' ---------------------------------------------------------------------'''
    def startMimeInfo(self, attrs=None):
        self.__currentElement = self.__currentArticle
        self.__currentMime = None

    def endMimeInfo(self, attrs=None):
        self.__currentMime = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Bild '''
    def createMime(self, attrs):
        self._objectIsNotNone(self.__currentMime,
                              "Fehler im BMEcat: Neues Bild soll erstellt werden. Es wird schon ein Bild verarbeitet.",
                              True)
        self.__currentMime = Mime()

    ''' Bild speichern '''
    def saveMime(self, attrs):
        if self._objectIsNotNone(self.__currentElement, "Bild konnte nicht gespeichert werden.", False):
            self.__currentElement.addMime(self.__currentMime, raiseException=False)
        self.__currentMime = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang TreatmentClass '''
    def createTreatmentClass(self, attrs):
        self._objectIsNotNone(self.__currentTreatmentClass,
                              "Fehler im BMEcat: Neue SpecialTreatmentClass soll erstellt werden. Es wird schon ein SpecialTreatmentClass verarbeitet.",
                              True)
        self.__currentTreatmentClass = TreatmentClass(attrs.getValue('type'))
        self.__currentElement = self.__currentTreatmentClass

    ''' TreatmentClass speichern '''
    def saveTreatmentClass(self, attrs):
        self._objectIsNone(self.__currentArticle,
                           "SpecialTreatmentClass soll gespeichert werden. Aber es ist kein Artikel vorhanden",
                           True)
        self.__currentTreatmentClass.value = self.__currentContent
        self.__currentArticle.addSpecialTreatmentClass(self.__currentTreatmentClass)
        self.__currentTreatmentClass = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    def createFeatureSet(self, attrs=None):
        self._objectIsNotNone(self.__currentFeature,
                              "Fehler im BMEcat: Neues Attributset soll erstellt werden. Es wird schon ein Attributset verarbeitet.",
                              True)
        self.__currentFeatureSet = FeatureSet()
        self.__currentContent = ""

    def saveFeatureSet(self, attrs=None):
        self._objectIsNone(self.__currentArticle,
                           "Attributset soll gespeichert werden. Aber es ist kein Artikel vorhanden", True)
        self.__currentArticle.addFeatureSet(self.__currentFeatureSet)
        self.__currentFeatureSet = None

    ''' ---------------------------------------------------------------------'''
    def createFeature(self, attrs=None):
        self._objectIsNotNone(self.__currentFeature, "Fehler im BMEcat: Neues Attribut soll erstellt werden. Es wird schon ein Attribut verarbeitet.", True)
        self.__currentFeature = Feature()
        self.__currentElement = self.__currentFeature
        self.__currentContent = ""

    def saveFeature(self, attrs=None):
        if not self._objectIsNone(self.__currentFeatureSet, "Attribut soll gespeichert werden. Aber es ist kein Attributset vorhanden", False):
            self.__currentFeatureSet.addFeature(self.__currentFeature)

        self.__currentFeature = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Referenz erstellen'''
    def createReference(self, attrs=None):
        self._objectIsNotNone(self.__currentReference,
                              "Fehler im BMEcat: Neue Referenz soll erstellt werden. Es wird schon eine Referenz verarbeitet.",
                              True)
        if 'type' not in attrs.getNames():
            logging.warning("Referenz auf Artikel konnte nicht verarbeitet werdern, da kein Typ angegeben wurde.")
        else:
            self.__currentReference = Reference()
            self.__currentElement = self.__currentReference
            self.__currentReference.referenceType = attrs.getValue('type')
            if 'quantity' in attrs.getNames():
                self.__currentReference.quantity = attrs.getValue('quantity')

    ''' Referenz speichern'''
    def saveReference(self, attrs=None):
        self.save(self.__currentReference, self.__currentArticle, "references")
        # self.__currentArticle.addReference(self.__currentReference)
        self.__currentReference = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Erstellen '''
    def create(self, typeToCreate, referenceToSet, setCurrentElement=False):
        self._objectIsNotNone(referenceToSet,
                              "Fehler im BMEcat: Neues Bild soll erstellt werden. Es wird schon ein Bild verarbeitet.", True)
        referenceToSet = typeToCreate()
        if setCurrentElement:
            self.__currentElement = referenceToSet

    ''' speichern '''
    def save(self, elementToBeSaved, elementToSaveAt, attributeName):
        if not isinstance(elementToSaveAt, ValidatingObject):
            logging.warning("'{0}' konnte nicht gespeichert werden.".format(elementToBeSaved.__class__.__name__))
        else:
            elementToSaveAt.add(attributeName, elementToBeSaved)

    ''' ---------------------------------------------------------------------'''
    def _addAttribute(self, elementWithAddMethod, attrName, raiseException):
        if self._objectIsNone(elementWithAddMethod,
                              "{0} soll gespeichert werden. Aber es ist kein {1} vorhanden.".format(attrName, elementWithAddMethod.__class__.__name__),
                              raiseException) or self._noValidatingObject(elementWithAddMethod,
                                                                          "Could not execute addMethod. No ValidatingObject",
                                                                          raiseException):
            return
        elementWithAddMethod.add(attrName, self.__currentContent)
        if self.__currentArticle is not None:
            logging.debug("Artikel '{0}': {1} ".format(attrName, self.__currentArticle.productId))
        if attrName.startswith('description'):
            self.__lineFeedToHTML = False

    def _addAttributeToCurrentArticle(self, attrName, raiseException):
        self._addAttribute(self.__currentArticle, attrName, raiseException)

    def _addAttributeToCurrentArticleDetails(self, attrName, raiseException):
        self.__currentArticle.addDetails()
        self._addAttribute(self.__currentArticleDetails, attrName, raiseException)

    def _addAttributeToCurrentArticleOrderDetails(self, attrName, raiseException):
        self._addAttribute(self.__currentOrderDetails, attrName, raiseException)

    def _addAttributeToCurrentPrice(self, attrName, raiseException):
        if attrName in self.__fieldsToTransform:
            self.__currentContent = self. _separatorTransformer.transform(self.__currentContent)
        self._addAttribute(self.__currentPrice, attrName, raiseException)

    def _addAttributeToCurrentMime(self, attrName, raiseException):
        self._addAttribute(self.__currentMime, attrName, raiseException)

    def _addAttributeToCurrentFeatureSet(self, attrName, raiseException):
        self._addAttribute(self.__currentFeatureSet, attrName, raiseException)

    def _addAttributeToCurrentFeature(self, attrName, raiseException):
        self._addAttribute(self.__currentFeature, attrName, raiseException)

    def _addAttributeToCurrentElement(self, attrName, raiseException):
        self._addAttribute(self.__currentElement, attrName, raiseException)

    ''' Attribut fuer Variante speichern '''
    def _addAttributeToCurrentVariant(self, attrName, raiseException):
        self._addAttribute(self.__currentVariant, attrName, raiseException)

    ''' ---------------------------------------------------------------------'''
    ''' Referenz ID speichern'''
    ''' Referenz Beschreibung speichern'''
    def _addAttributeToCurrentReference(self, attrName, raiseException):
        self._addAttribute(self.__currentReference, attrName, raiseException)

    ''' ---------------------------------------------------------------------'''
    def _startDescription(self, attrs=None):
        self.__lineFeedToHTML = True

    ''' ---------------------------------------------------------------------'''
    def createFeatureVariantSet(self, attrs=None):
        self._objectIsNotNoneAndNotEmpty(self.__currentFeature.values ,
                                         "Fehler im BMEcat: FeatureVariants sollen hinzugefuegt werden, es existieren aber schon FeatureValues.",
                                         True)
        self._objectIsNotNone(self.__currentFeature.variants,
                              "Fehler im BMEcat: FeatureVariants sollen hinzugefuegt werden, es existieren aber schon FeatureVariants.")
        self.__currentFeature.addVariantSet()

    def addFeatureVariantSetOrder(self, attrs=None):
        self.__currentFeature.addVariantOrder(int(self.__currentContent))

    def createFeatureVariant(self, attrs=None):
        self._objectIsNotNone(self.__currentVariant,
                              "Fehler im BMEcat: FeatureVariant soll erstellt werden, aber es existiert schon eine.")
        self.__currentVariant = Variant()
        self.__currentElement = self.__currentVariant

    def saveFeatureVariant(self, attrs=None):
        self.__currentFeature.addVariant(self.__currentVariant)
        self.__currentVariant = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    def startDateTime(self, attrs=None):
        if attrs is None or 'type' not in attrs.getNames():
            logging.warning("DateTime kann nicht gespeichert werden.")
        else:
            self.__dateType = attrs.getValue('type')
            self.__currentElement = self.__currentPriceDetails

    def endDateTime(self, attrs=None):
        self.__dateType = None
        self.__currentElement = None

    def addDate(self, attrs=None):
        if self.__currentElement is None:
            logging.warning("Datum [" + self.__dateType + "] kann nicht gespeichert werden, weil kein Element zum Speichern existiert.")
        elif self.__dateType is None:
            logging.warning("Kein Datumstyp gesetzt. Datum kann nicht gespeichert werden.")
        elif self.__dateType == 'valid_start_date':
            logging.debug("Datum [" + self.__currentContent + "] wird als Startdatum gespeichert.")
            self.__currentElement.validFrom = datetime.strptime(self.__currentContent, self.__dateFormat)
        elif self.__dateType == 'valid_end_date':
            logging.debug("Datum [" + self.__currentContent + "] wird als Enddatum gespeichert.")
            self.__currentElement.validTo = datetime.strptime(self.__currentContent, self.__dateFormat)
        else:
            logging.warning("Datum [" + self.__dateType + "] kann nicht gespeichert werden.")

    ''' ---------------------------------------------------------------------'''
    '''aktuellen Inhalt des XML-Elements ermitteln'''
    def characters(self, content):
        logging.debug("Original input: '{0}'".format(content))
        if self.__lineFeedToHTML:
            self.__currentContent += content.replace("\n", "<br>").strip()
        else:
            if len(self.__currentContent) > 0 and len(content) > len(content.strip()):
                self.__currentContent = self.__currentContent.strip() + ' '
            self.__currentContent += content.strip()
        logging.debug("Saved input: '{0}'".format(self.__currentContent))

    def _noValidatingObject(self, elementToCheck, msg, raiseException):
        if not isinstance(elementToCheck, ValidatingObject):
            if raiseException:
                raise Exception(msg)
            else:
                logging.warning(msg)
                return True
        return False

    def _objectIsNone(self, objectToCheck, msg, raiseException):
        if objectToCheck is None:
            if raiseException:
                raise Exception(msg)
            else:
                logging.warning(msg)
                return True
        return False

    def _objectIsNotNone(self, objectToCheck, msg, raiseException):
        if objectToCheck is not None:
            if raiseException:
                raise Exception(msg)
            else:
                logging.warning(msg)
                return True
        return False

    def _objectIsNotNoneAndNotEmpty(self, objectToCheck, msg, raiseException):
        self._objectIsNotNone(objectToCheck, msg)
        if isinstance(objectToCheck, (list, array)) and len(objectToCheck) > 0:
            if raiseException:
                raise Exception(msg)
            else:
                logging.warning(msg)
                return True
        return False
