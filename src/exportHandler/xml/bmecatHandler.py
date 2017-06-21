'''
Created on 12.05.2017

@author: henrik.pilz
'''
from xml.sax import handler
from datetime import datetime

from data.product import Product
from data.productDetails import ProductDetails
from data.price import Price
from data.priceDetails import PriceDetails
from data.orderDetails import OrderDetails
from data.feature import Feature
from data.featureSet import FeatureSet
from data.mime import Mime
from data.treatmentClass import TreatmentClass
from data.reference import Reference

import logging

class BMEcatHandler(handler.ContentHandler):
    
    ''' alle registrierten StartElementhandler '''
    _startElementHandler = {
                "article" : "createProduct",
                "article_details" : "createProductDetails", 
                "order_details" : "createOrderDetails",
                "price_details" : "createPriceDetails",
                "price" : "createPrice",                
                "mime" : "createMime",
                "mime_info" : "startMimeInfo",
                "datetime" : "startDateTime",
                "article_features" :"createFeatureSet",
                "feature" : "createFeature",
                "special_treatment_class" : "createTreatmentClass",
                "article_reference" : "createReference" 
                }

    ''' Mögliche Aliase für Varianten der BMEcats '''
    _alias = {
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
                "prod_id_to" : "art_id_to"
            }
            
    ''' alle registrierten EndElementhandler '''
    _endElementHandler = {
                "article_features" :"saveFeatureSet",
                "feature" : "saveFeature",
                "article" : "saveProduct",
                "mime_info" : "endMimeInfo",
                "datetime" : "endDateTime",
                "mime" : "saveMime",
                "supplier_aid" : "addArticleId",
                "supplier_alt_aid" : "addAlternativeArticleId",
                "buyer_aid" : "addAlternativeArticleId",
                "manufacturer_aid" : "addManufacturerArticleId",
                "manufacturer_name" : "addManufacturerName",
                "ean" : "addEAN", 
                "description_long" : "addDescription",
                "description_short" : "addTitle",
                "price" : "savePrice",
                "price_details" : "savePriceDetails",
                "delivery_time" : "addDeliveryTime",
                "price_amount" : "addPriceAmount",
                "tax" : "addPriceTax",
                "price_currency" : "addPriceCurrency",
                "price_factor" : "addPriceFactor",
                "territory" : "addTerritory",
                "lower_bound" : "addPriceLowerBound",
                "mime_source" : "addMimeSource",
                "mime_type" : "addMimeType",
                "mime_descr" : "addMimeDescription",
                "mime_alt" : "addMimeAlt",
                "mime_purpose" : "addMimePurpose",
                "mime_order" : "addMimeOrder",
                "order_unit" : "addOrderUnit",
                "content_unit" : "addContentUnit",
                "no_cu_per_ou " : "addPackagingQuantity",
                "price_quantity " : "addPriceQuantity",
                "quantity_min " : "addQuantityMin",
                "quantity_interval" : "addQuantityInterval",
                "date" : "addDate",
                "fname" : "addFeatureName",
                "fvalue" : "addFeatureValue",
                "fvalue_details" : "addFeatureValueDetails",
                "funit" : "addFeatureUnit",
                "fdesc" : "addFeatureDescription",
                "special_treatment_class" : "saveTreatmentClass",
                "catalog_group_system" : "resetAll",
                "article_reference" : "saveReference",
                "art_id_to" : "addReferenceArticleId",
                "reference_descr" : "addReferenceDescription"
                }
    
    ''' Handlernamen für das XML-Element ermitteln. '''
    def determinteHandlername(self, tag, bOpen):
        name = tag.lower()
        if tag.lower() in self._alias:
            logging.debug("[" + str(bOpen) +"] '" + tag + "' has an alias")
            name = self._alias[tag.lower()]

        handlerName = None
        if bOpen:
            try:
                handlerName = self._startElementHandler[name]
            except KeyError:
                logging.debug("Call for Start Tag <" + name + "> FAILED:")            
        else :
            try:
                handlerName = self._endElementHandler[name]
            except KeyError:
                logging.debug("Call for End Tag <" + name + "> FAILED:")            
        return handlerName

    ''' Konstruktor '''
    def __init__(self, dateFormat, decimalSeparator, thousandSeparator):
        self._dateFormat=dateFormat 
        self._decimalSeparator = decimalSeparator
        self._thousandSeparator = thousandSeparator
        
        if self._decimalSeparator is None or self._thousandSeparator  is None:
            raise Exception("Dezimaltrennzeichen und Tausendertrennzeichen müssen angegeben werden.")
        if self._decimalSeparator==self._thousandSeparator:
            raise Exception("Dezimaltrennzeichen und Tausendertrennzeichen dürfen nicht gleich sein.")
        
        '''articles by SKU and Product Structure as Value'''
        self._articles = { "new" : [], "update" : [], "delete" : [] }
        self._currentArticle = None
        self._currentPrice = None
        self._currentMime = None
        self._currentPriceDetails = None
        self._currentElement = None
        self._currentContent = ""
        self._dateType = None
        self._currentFeatureSet = None
        self._currentFeature = None
        self._currentTreatmentClass = None
        self._currentReference = None
  
  
    ''' Starte aktuelles XML Element '''
    def startElement(self, name, attrs):
        self.workOnElement(name, attrs, True)

    ''' Schließe aktuelles XML Element '''
    def endElement(self, name):
        self.workOnElement(name, None, False)
    
    ''' Handler ermitteln, der die Arbeit macht. '''
    def workOnElement(self, name, attrs, bOpen):
        logging.debug("Call for Tag <" + name + ">")
        elementHandler = None
        try:
            handlerName = self.determinteHandlername(name, bOpen)
            if not handlerName is None:
                elementHandler = getattr(self, handlerName)
                elementHandler(attrs)
            self._currentContent = ""
        except AttributeError:
            raise NotImplementedError("Class [" + self.__class__.__name__ + "] does not implement [" + handlerName + "]")

    ''' ---------------------------------------------------------------------'''
    def resetAll(self, attrs=None):
        self._currentArticle = None
        self._currentPrice = None
        self._currentMime = None
        self._currentPriceDetails = None
        self._currentElement = None
        self._currentContent = ""
        self._dateType = None
        self._currentFeatureSet = None
        self._currentFeature = None
        self._currentTreatmentClass = None

    ''' ---------------------------------------------------------------------'''
    def startMimeInfo(self, attrs=None):
        self._currentElement = self._currentArticle
        
    def endMimeInfo(self, attrs=None):
        self._currentMime = None
        self._currentElement = None
    
    ''' ---------------------------------------------------------------------'''
    ''' Anfang Artikel '''
    def createProduct(self, attrs):
        logging.info("Anfang Produkt " + ", ".join(attrs.getNames()))
        if not self._currentArticle is None:
            raise Exception("Fehler im BMEcat: Neuer Artikel soll erstellt werden. Es wird schon ein Artikel verarbeitet.")
        else:
            self._currentArticle = Product()
            self._currentContent = ""
            self._currentElement = self._currentArticle
            articleMode = 'new'
            if 'mode' in attrs.getNames():
                articleMode = attrs.getValue('mode')
            else:
                logging.warning("Fehler im BMEcat: es wurde kein mode für den Artikel angegeben.")
            logging.info("Neues Produkt erstellt. Modus: " + articleMode)
            self._articles[articleMode].append(self._currentArticle)

    ''' Artikel speichern '''
    def saveProduct(self, attr=None):
        logging.info("Produkt validieren: " + self._currentArticle.productId)
        self.validateCurrentProduct()
        logging.info("Produktende")
        self.resetAll()

    ''' ---------------------------------------------------------------------'''
    def createProductDetails(self, attrs):
        if self._currentArticle is None:
            raise Exception("Artikeldetails sollen erstellt werden. Aber es ist kein Artikel vorhanden")
        if not self._currentArticle.details is None:
            raise Exception("Fehler im BMEcat: Neue Artikeldetails sollen erstellt werden. Es werden schon Artikeldetails verarbeitet.")
        else:
            self._currentArticle.details = ProductDetails()

    ''' ---------------------------------------------------------------------'''
    def createOrderDetails(self, attrs):
        if self._currentArticle is None:
            raise Exception("Bestelldetails sollen erstellt werden. Aber es ist kein Artikel vorhanden")
        if not self._currentArticle.orderDetails is None:
            raise Exception("Fehler im BMEcat: Neue Bestelldetails sollen erstellt werden. Es werden schon Bestelldetails verarbeitet.")
        else: 
            self._currentArticle.orderDetails = OrderDetails()

    ''' ---------------------------------------------------------------------'''
    def createPriceDetails(self, attrs):
        if not self._currentPriceDetails is None:
            raise Exception("Fehler im BMEcat: Neue Preisdetails sollen erstellt werden. Es werden schon Preisdetails verarbeitet.") 
        else: 
            self._currentPriceDetails = PriceDetails()
            self._currentElement = self._currentPriceDetails

    def savePriceDetails(self, attrs):
        if self._currentArticle is None:
            raise Exception("Preisdetails sollen gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addPriceDetails(self._currentPriceDetails)
        self._currentPriceDetails = None
        self._currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Bild '''
    def createMime(self, attrs):
        if not self._currentMime is None:
            raise Exception("Fehler im BMEcat: Neues Bild soll erstellt werden. Es wird schon ein Bild verarbeitet.")
        else: 
            self._currentMime = Mime()

    ''' Bild speichern '''
    def saveMime(self, attrs):
        if self._currentElement is None:
            logging.warning("Bild konnte nicht gespeichert werden.")
        else:
            self._currentElement.addMime(self._currentMime)
        self._currentMime = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Preis '''
    def createPrice(self, attrs):
        if not self._currentPrice is None:
            raise Exception("Fehler im BMEcat: Neuer Preis soll erstellt werden. Es wird schon ein Preis verarbeitet.")
        else: 
            self._currentPrice = Price()
            self._currentPrice.priceType = attrs.getValue('price_type')
            self._currentElement = self._currentPrice

    ''' Preis speichern '''
    def savePrice(self, attrs):
        if self._currentPriceDetails is None:
            raise Exception("Preis soll gespeichert werden. Aber es sind keine Preisdetails  vorhanden")
        self._currentPriceDetails.prices.append(self._currentPrice)
        self._currentPrice = None
        self._currentElement = self._currentPriceDetails     


    ''' ---------------------------------------------------------------------'''
    ''' Anfang TreatmentClass '''
    def createTreatmentClass(self, attrs):
        if not self._currentTreatmentClass is None:
            raise Exception("Fehler im BMEcat: Neue SpecialTreatmentClass soll erstellt werden. Es wird schon ein SpecialTreatmentClass verarbeitet.")
        else: 
            self._currentTreatmentClass = TreatmentClass()
            self._currentTreatmentClass.classType = attrs.getValue('type')
            self._currentElement = self._currentTreatmentClass

    ''' TreatmentClass speichern '''
    def saveTreatmentClass(self, attrs):
        if self._currentArticle is None:
            raise Exception("SpecialTreatmentClass soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentTreatmentClass.value = self._currentContent
        self._currentArticle.addSpecialTreatmentClass(self._currentTreatmentClass)
        self._currentTreatmentClass = None
        self._currentElement = None

    ''' ---------------------------------------------------------------------'''
    def createFeatureSet(self, attrs=None):
        if not self._currentFeature is None:
            raise Exception("Fehler im BMEcat: Neues Attributset soll erstellt werden. Es wird schon ein Attributset verarbeitet.")
        else: 
            self._currentFeatureSet = FeatureSet()
            self._currentContent = ""

    def saveFeatureSet(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Attributset soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.featureSets.append(self._currentFeatureSet)
        self._currentFeatureSet = None

    ''' ---------------------------------------------------------------------'''
    def createFeature(self, attrs=None):
        if not self._currentFeature is None:
            raise Exception("Fehler im BMEcat: Neues Attribut soll erstellt werden. Es wird schon ein Attribut verarbeitet.")
        else: 
            self._currentFeature = Feature()
            self._currentContent = ""

    def saveFeature(self, attrs=None):
        if self._currentFeatureSet is None:
            raise Exception("Attribut soll gespeichert werden. Aber es ist kein Attributset vorhanden")
        self._currentFeatureSet.features.append(self._currentFeature)
        self._currentFeature = None

    ''' ---------------------------------------------------------------------'''
    ''' Referenz erstellen'''
    def createReference(self, attrs=None):
        if not self._currentReference is None:
            raise Exception("Fehler im BMEcat: Neue Referenz soll erstellt werden. Es wird schon eine Referenz verarbeitet.")
        if not 'type' in attrs.getNames():
            logging.warning("Referenz auf Artikel konnte nicht verarbeitet werdern, da kein Typ angegeben wurde.")
        else:
            self._currentReference = Reference()
            self._currentElement = self._currentReference
            self._currentReference.referenceType = attrs.getValue('type')
            if 'quantity' in attrs.getNames():
                self._currentReference.quantity = attrs.getValue('quantity')
                
    ''' Referenz speichern'''
    def saveReference(self, attrs=None):
        self._currentArticle.references.append(self._currentReference)
        self._currentReference = None
        self._currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Referenz ID speichern'''
    def addReferenceArticleId(self, attrs=None):
        self._currentReference.supplierArticleIds.append(self._currentContent)
        
    ''' Referenz Beschreibung speichern'''
    def addReferenceDescription(self, attrs=None):
        self._currentReference.description = self._currentContent
        
        
    ''' ---------------------------------------------------------------------'''
    ''' Artikelnummer speichern'''
    def addArticleId(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Artikelnummer soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        logging.info("Artikelnummer " + self._currentContent)
        self._currentArticle.productId = self._currentContent

    ''' HerstellerArtikelnummer speichern'''
    def addManufacturerArticleId(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Herstellerartikelnummer soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addManufacturerId(self._currentContent)

    def addManufacturerName(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Herstellername soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addManufacturerName(self._currentContent)

    def addEAN(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("EAN soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addEAN(self._currentContent)

    def addTitle(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Artikelname soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addTitle(self._currentContent)

    def addDescription(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Artikelbeschreibung soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addDescription(self._currentContent)

    def addAlternativeArticleId(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Alternative Herstellerartikelnummer soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        if self._currentArticle.productId is None:
            logging.info("Alternative Artikelnummer als Artikelnummer gesetzt!")
            self._currentArticle.productId = self._currentContent
        if self._currentArticle.details is None:
            raise Exception("Alternative Herstellerartikelnummer soll gespeichert werden. Aber es sind keine Artikeldetails vorhanden")
        else:
            logging.info("Alternative Artikelnummer: " + self._currentContent)
            self._currentArticle.details.supplierAltId = self._currentContent
        
    def addDeliveryTime(self, attrs=None):
        if self._currentArticle is None:
            raise Exception("Lieferzeit soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self._currentArticle.addDeliveryTime(self._currentContent)

    ''' ---------------------------------------------------------------------'''
    def convertToEnglishDecimalValue(self, stringValue):
        convertedString = stringValue
        if not self._decimalSeparator == ".": 
            convertedString = convertedString.replace(",",";").replace(self._thousandSeparator,"").replace(";",".")
        return convertedString


    ''' ---------------------------------------------------------------------'''
    def addPriceAmount(self, attrs=None):
        self._currentPrice.amount = self.convertToEnglishDecimalValue(self._currentContent)

    def addPriceCurrency(self, attrs=None):
        self._currentPrice.currency = self._currentContent

    def addPriceTax(self, attrs=None):
        stringValue = self._currentContent.replace("%", "").strip()
        convertedValue = float(self.convertToEnglishDecimalValue(stringValue))
        if convertedValue > 1:
            convertedValue = convertedValue / 100
        self._currentPrice.tax = convertedValue

    def addPriceFactor(self, attrs=None):
        self._currentPrice.factor = self.convertToEnglishDecimalValue(self._currentContent)
    
    def addPriceLowerBound(self, attrs=None):
        self._currentPrice.lowerBound = self._currentContent
        
    ''' ---------------------------------------------------------------------'''
    def addTerritory(self, attrs=None):
        if self._currentElement is None:
            logging.warning("Territory kann nicht gespeichert werden.")
        else:
            self._currentElement.territory = self._currentContent

    ''' ---------------------------------------------------------------------'''
    def addMimeSource(self, attrs=None):
        self._currentMime.source = self._currentContent

    def addMimeType(self, attrs=None):
        self._currentMime.mimeType = self._currentContent

    def addMimeAlt(self, attrs=None):
        self._currentMime.altenativeContent = self._currentContent

    def addMimePurpose(self, attrs=None):
        self._currentMime.purpose = self._currentContent

    def addMimeDescription(self, attrs=None):
        self._currentMime.description = self._currentContent

    def addMimeOrder(self, attrs=None):
        self._currentMime.order = self._currentContent
    
    ''' ---------------------------------------------------------------------'''
    def addOrderUnit(self, attrs=None):
        self._currentArticle.orderDetails.orderUnit = self._currentContent
    
    def addContentUnit(self, attrs=None):
        self._currentArticle.orderDetails.contentUnit = self._currentContent

    def addPriceQuantity(self, attrs=None):
        self._currentArticle.orderDetails.priceQuantity = self._currentContent
        
    def addPackagingQuantity(self, attrs=None):
        self._currentArticle.orderDetails.packagingQuantity = self._currentContent

    def addQuantityInterval(self, attrs=None):
        self._currentArticle.orderDetails.quantityInterval = self._currentContent

    def addQuantityMin(self, attrs=None):
        self._currentArticle.orderDetails.quantityMin = self._currentContent
        
    ''' ---------------------------------------------------------------------'''
    def addFeatureValue(self, attrs = None):
        self._currentFeature.value = self._currentContent

    def addFeatureUnit(self, attrs = None):
        self._currentFeature.unit = self._currentContent

    def addFeatureName(self, attrs = None):
        self._currentFeature.name = self._currentContent

    def addFeatureDescription(self, attrs = None):
        self._currentFeature.description = self._currentContent

    
    def startDateTime(self, attrs = None):
        if attrs is None or not 'type' in attrs.getNames():
            logging.warning("DateTime kann nicht gespeichert werden.")
        else:
            self._dateType = attrs.getValue('type')
            self._currentElement = self._currentPriceDetails
    
    def endDateTime(self, attrs = None):
        self._dateType = None
        self._currentElement = None
    
    def addDate(self, attrs=None):
        if self._dateType is None:
            logging.warning("Datum kann nicht gespeichert werden.")
        elif self._currentElement is None:
            logging.warning("Datum [" + self._dateType + "] kann nicht gespeichert werden, weil kein Element zum Speichern existiert.")
        else:
            if self._dateType == 'valid_start_date':
                self._currentElement.validFrom = datetime.strptime(self._currentContent, self._dateFormat)
            elif self._dateType == 'valid_end_date':
                self._currentElement.validTo = datetime.strptime(self._currentContent, self._dateFormat)
            else:
                logging.warning("Datum [" + self._dateType + "] kann nicht gespeichert werden.")

        
    ''' ---------------------------------------------------------------------'''
    '''aktuellen Inhalt des XML-Elements ermitteln'''
    def characters(self, content):        
        self._currentContent += content.strip()        

    def validateCurrentProduct(self):
        if self._currentArticle is None:
            raise Exception("Es wurde kein aktuell zu bearbeitender Artikel gefunden.")
        self._currentArticle.validate()