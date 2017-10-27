'''
Created on 05.05.2017

@author: henrik.pilz
'''
from datetime import datetime
import logging
import os
from xml.sax import handler

from datamodel import Feature, FeatureSet, Mime, OrderDetails, Price, PriceDetails, Product, ProductDetails, Reference, TreatmentClass, Variant, VariantSet
from mapping import Blacklist, UnitMapper


class BMEcatImportHandler(handler.ContentHandler):
    '''
        Handler fuer Sax2Parser, welcher BMEcats in den Formaten 1.01,1.2,2005, 2005.1 sowie ETIM aller Arten liest.
    '''
    
    ''' alle registrierten StartElementhandler '''
    __startElementHandler = {
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
                "article_reference" : "createReference",
                "variants" : "createFeatureVariantSet",
                "variant" : "createFeatureVariant",
                "description_long" : "startDescription"
                }

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
                "description_long" : "saveDescription",
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
                "no_cu_per_ou" : "addPackagingQuantity",
                "price_quantity" : "addPriceQuantity",
                "quantity_min" : "addQuantityMin",
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
                "reference_descr" : "addReferenceDescription",
                "variants" : "saveFeatureVariantSet",
                "vorder" : "addFeatureVariantSetOrder",
                "variant" : "addFeatureVariant",
                "supplier_aid_supplement" : "addFeatureVariantProductIdSuffix",
                "reference_feature_system_name" : "addFeatureSetReferenceSystem",
                "reference_feature_group_id" : "addFeatureSetReferenceGroupId"
                }
    
    __baseDirectory = os.path.join(os.path.dirname(__file__),"..","..", "..","documents","BMEcat","version")
    __bmecatUnitMapper = UnitMapper(os.path.join(__baseDirectory, "BMEcatUnitMapping.csv"))
    __etimUnitMapper = UnitMapper(os.path.join(__baseDirectory, "ETIMUnitMapping.csv"))
    
    __featureSetBlacklist = Blacklist(os.path.join(__baseDirectory, "FeatureSetBlacklist.csv"))
    __featureBlacklist = Blacklist(os.path.join(__baseDirectory, "FeatureBlacklist.csv"))
    
    
    ''' Handlernamen fuer das XML-Element ermitteln. '''

    def __determineTagName(self, tag, bOpen):
        name = tag.lower()
        if tag.lower() in self.__alias:
            logging.debug("[" + str(bOpen) + "] '" + tag + "' has an alias")
            name = self.__alias[tag.lower()]
        return name

    def __determineTagHandlername(self, tag, bOpen):
        name = self.__determineTagName(tag, bOpen)
        if bOpen:
            return self.__determineHandlername(name, self.__startElementHandler)
        else:
            return self.__determineHandlername(name, self.__endElementHandler)

    def __determineHandlername(self, name, handlerByName):
            try:
                return handlerByName[name]
            except KeyError:
                logging.debug("Call for Tag <" + name + "> FAILED:")       

    ''' Konstruktor '''
    def __init__(self, dateFormat, decimalSeparator, thousandSeparator):
        self.__dateFormat=dateFormat
        '''self.__separatorConverter = SeparatorConverter()'''

        self.__decimalSeparator = decimalSeparator
        self.__thousandSeparator = thousandSeparator
        
        if self.__decimalSeparator is None or self.__thousandSeparator  is None:
            raise Exception("Dezimaltrennzeichen und Tausendertrennzeichen muessen angegeben werden.")
        if self.__decimalSeparator==self.__thousandSeparator:
            raise Exception("Dezimaltrennzeichen und Tausendertrennzeichen duerfen nicht gleich sein.")
        
        '''articles by SKU and Product Structure as Value'''
        self.articles = { "new" : [], "update" : [], "delete" : [], "failed" : [] }
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
        self.__currentReference = None
        self.__currentVariant = None
        self.__lineFeedToHTML = False
        self.__currentArticleMode = "failed"
  
    ''' Starte aktuelles XML Element '''
    def startElement(self, name, attrs):
        self.__workOnElement(name, attrs, True)

    ''' Schliesse aktuelles XML Element '''
    def endElement(self, name):
        self.__workOnElement(name, None, False)
    
    ''' Handler ermitteln, der die Arbeit macht. '''
    def __workOnElement(self, name, attrs, bOpen):
        logging.debug("Call for Tag <" + name + ">")
        elementHandler = None
        try:
            handlerName = self.__determineTagHandlername(name, bOpen)
            if not handlerName is None:
                elementHandler = getattr(self, handlerName)
                elementHandler(attrs)
            self.__currentContent = ""
        except AttributeError:
            raise NotImplementedError("Class [" + self.__class__.__name__ + "] does not implement [" + handlerName + "]")

    ''' ---------------------------------------------------------------------'''
    def resetAll(self, attrs = None):
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
    def startMimeInfo(self, attrs = None):
        self.__currentElement = self.__currentArticle
        
    def endMimeInfo(self, attrs = None):
        self.__currentMime = None
        self.__currentElement = None
    
    ''' ---------------------------------------------------------------------'''
    ''' Anfang Artikel '''
    def createProduct(self, attrs):
        logging.debug("Anfang Produkt " + ", ".join(attrs.getNames()))
        if not self.__currentArticle is None:
            raise Exception("Fehler im BMEcat: Neuer Artikel soll erstellt werden. Es wird schon ein Artikel verarbeitet.")
        else:
            self.__currentArticle = Product()
            self.__currentContent = ""
            self.__currentElement = self.__currentArticle
            self.__currentArticleMode = 'new'
            if 'mode' in attrs.getNames():
                self.__currentArticleMode = attrs.getValue('mode')
            else:
                logging.warning("Fehler im BMEcat: es wurde kein mode fuer den Artikel angegeben.")

    ''' Artikel speichern '''
    def saveProduct(self, attr=None):
        if self.__currentArticle.productId is None:            
            '''self.articles["failed"].append(self.__currentArticle)'''
            logging.error("Produkt konnte nicht gespeichert werden. Fehlerhafte Daten: Keine Artikelnummer.")
        else:
            logging.info("Produkt validieren: " + self.__currentArticle.productId)
            self.validateCurrentProduct()
            logging.debug("Neues Produkt erstellt. Modus: " + self.__currentArticleMode)
            self.articles[self.__currentArticleMode].append(self.__currentArticle)
        logging.debug("Produktende")
        self.resetAll()

    ''' ---------------------------------------------------------------------'''
    def createProductDetails(self, attrs):
        if self.__currentArticle is None:
            raise Exception("Artikeldetails sollen erstellt werden. Aber es ist kein Artikel vorhanden")
        if not self.__currentArticle.details is None:
            raise Exception("Fehler im BMEcat: Neue Artikeldetails sollen erstellt werden. Es werden schon Artikeldetails verarbeitet.")
        else:
            self.__currentArticle.details = ProductDetails()

    ''' ---------------------------------------------------------------------'''
    def createOrderDetails(self, attrs):
        if self.__currentArticle is None:
            raise Exception("Bestelldetails sollen erstellt werden. Aber es ist kein Artikel vorhanden")
        if not self.__currentArticle.orderDetails is None:
            raise Exception("Fehler im BMEcat: Neue Bestelldetails sollen erstellt werden. Es werden schon Bestelldetails verarbeitet.")
        else: 
            self.__currentArticle.orderDetails = OrderDetails()

    ''' ---------------------------------------------------------------------'''
    def createPriceDetails(self, attrs):
        if not self.__currentPriceDetails is None:
            raise Exception("Fehler im BMEcat: Neue Preisdetails sollen erstellt werden. Es werden schon Preisdetails verarbeitet.") 
        else: 
            self.__currentPriceDetails = PriceDetails()
            self.__currentElement = self.__currentPriceDetails

    def savePriceDetails(self, attrs):
        if self.__currentArticle is None:
            raise Exception("Preisdetails sollen gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addPriceDetails(self.__currentPriceDetails)
        self.__currentPriceDetails = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Bild '''
    def createMime(self, attrs):
        if not self.__currentMime is None:
            raise Exception("Fehler im BMEcat: Neues Bild soll erstellt werden. Es wird schon ein Bild verarbeitet.")
        else: 
            self.__currentMime = Mime()

    ''' Bild speichern '''
    def saveMime(self, attrs):
        if self.__currentElement is None:
            logging.warning("Bild konnte nicht gespeichert werden.")
        else:
            self.__currentElement.addMime(self.__currentMime, raiseException=False)
        self.__currentMime = None

    ''' ---------------------------------------------------------------------'''
    ''' Anfang Preis '''
    def createPrice(self, attrs):
        if not self.__currentPrice is None:
            raise Exception("Fehler im BMEcat: Neuer Preis soll erstellt werden. Es wird schon ein Preis verarbeitet.")
        else: 
            self.__currentPrice = Price()
            self.__currentPrice.priceType = attrs.getValue('price_type')
            self.__currentElement = self.__currentPrice

    ''' Preis speichern '''
    def savePrice(self, attrs):
        if self.__currentPriceDetails is None:
            raise Exception("Preis soll gespeichert werden. Aber es sind keine Preisdetails  vorhanden")
        self.__currentPriceDetails.prices.append(self.__currentPrice)
        self.__currentPrice = None
        self.__currentElement = self.__currentPriceDetails     


    ''' ---------------------------------------------------------------------'''
    ''' Anfang TreatmentClass '''
    def createTreatmentClass(self, attrs):
        if not self.__currentTreatmentClass is None:
            raise Exception("Fehler im BMEcat: Neue SpecialTreatmentClass soll erstellt werden. Es wird schon ein SpecialTreatmentClass verarbeitet.")
        else: 
            self.__currentTreatmentClass = TreatmentClass()
            self.__currentTreatmentClass.classType = attrs.getValue('type')
            self.__currentElement = self.__currentTreatmentClass

    ''' TreatmentClass speichern '''
    def saveTreatmentClass(self, attrs):
        if self.__currentArticle is None:
            raise Exception("SpecialTreatmentClass soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentTreatmentClass.value = self.__currentContent
        self.__currentArticle.addSpecialTreatmentClass(self.__currentTreatmentClass)
        self.__currentTreatmentClass = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    def createFeatureSet(self, attrs = None):
        if not self.__currentFeature is None:
            raise Exception("Fehler im BMEcat: Neues Attributset soll erstellt werden. Es wird schon ein Attributset verarbeitet.")
        else: 
            self.__currentFeatureSet = FeatureSet()
            self.__currentContent = ""

    def saveFeatureSet(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Attributset soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        if len(self.__currentFeatureSet.features) < 1:
            logging.info("Attributset wird nicht gespeichert, da kein Attribute enthalten sind.")
        elif self.__featureSetBlacklist.contains(self.__currentFeatureSet.referenceSytem):
            logging.info("Attributset wird nicht gespeichert, da es auf der Blacklist ist.")
        else:
            self.__currentArticle.addFeatureSet(self.__currentFeatureSet)
        self.__currentFeatureSet = None
    
    def addFeatureSetReferenceSystem(self, attrs = None):
        if self.__currentFeatureSet is None:
            raise Exception("Referenzsystem soll gesetzt werden. Aber es ist kein Attributset vorhanden")                
        self.__currentFeatureSet.referenceSytem = self.__currentContent

    def addFeatureSetReferenceGroupId(self, attrs = None):
        if self.__currentFeatureSet is None:
            raise Exception("Gruppen ID soll gesetzt werden. Aber es ist kein Attributset vorhanden")                
        self.__currentFeatureSet.referenceGroupId = self.__currentContent

    ''' ---------------------------------------------------------------------'''
    def createFeature(self, attrs = None):
        if self.__currentFeature is not None:
            raise Exception("Fehler im BMEcat: Neues Attribut soll erstellt werden. Es wird schon ein Attribut verarbeitet.")
        else: 
            self.__currentFeature = Feature()
            self.__currentElement = self.__currentFeature
            self.__currentContent = ""

    def saveFeature(self, attrs = None):
        if self.__currentFeatureSet is None:
            raise Exception("Attribut soll gespeichert werden. Aber es ist kein Attributset vorhanden")
        elif self.__featureBlacklist.contains(self.__currentFeature.name):
            logging.info("Attribut wird nicht gespeichert, da es auf der Blacklist ist.")
        else:
            self.__currentFeatureSet.addFeature(self.__currentFeature)

        self.__currentFeature = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Referenz erstellen'''
    def createReference(self, attrs = None):
        if not self.__currentReference is None:
            raise Exception("Fehler im BMEcat: Neue Referenz soll erstellt werden. Es wird schon eine Referenz verarbeitet.")
        if not 'type' in attrs.getNames():
            logging.warning("Referenz auf Artikel konnte nicht verarbeitet werdern, da kein Typ angegeben wurde.")
        else:
            self.__currentReference = Reference()
            self.__currentElement = self.__currentReference
            self.__currentReference.referenceType = attrs.getValue('type')
            if 'quantity' in attrs.getNames():
                self.__currentReference.quantity = attrs.getValue('quantity')
                
    ''' Referenz speichern'''
    def saveReference(self, attrs = None):
        self.__currentArticle.references.append(self.__currentReference)
        self.__currentReference = None
        self.__currentElement = None

    ''' ---------------------------------------------------------------------'''
    ''' Referenz ID speichern'''
    def addReferenceArticleId(self, attrs = None):
        self.__currentReference.addSupplierArticleId(self.__currentContent)
        
    ''' Referenz Beschreibung speichern'''
    def addReferenceDescription(self, attrs = None):
        self.__currentReference.description = self.__currentContent
        
        
    ''' ---------------------------------------------------------------------'''
    ''' Artikelnummer speichern'''
    def addArticleId(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Artikelnummer soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        logging.debug("Artikelnummer " + self.__currentContent)
        self.__currentArticle.productId = self.__currentContent

    ''' HerstellerArtikelnummer speichern'''
    def addManufacturerArticleId(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Herstellerartikelnummer soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addManufacturerArticleId(self.__currentContent)

    def addManufacturerName(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Herstellername soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addManufacturerName(self.__currentContent)

    def addEAN(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("EAN soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addEAN(self.__currentContent)

    def addTitle(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Artikelname soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addTitle(self.__currentContent)

    def startDescription(self, attrs = None):
        self.__lineFeedToHTML = True
        
    def saveDescription(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Artikelbeschreibung soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addDescription(self.__currentContent)
        self.__lineFeedToHTML = False

    def addAlternativeArticleId(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Alternative Herstellerartikelnummer soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        if self.__currentArticle.productId is None:
            logging.info("Alternative Artikelnummer als Artikelnummer gesetzt!")
            self.__currentArticle.productId = self.__currentContent
        if self.__currentArticle.details is None:
            raise Exception("Alternative Herstellerartikelnummer soll gespeichert werden. Aber es sind keine Artikeldetails vorhanden")
        else:
            logging.debug("Alternative Artikelnummer: " + self.__currentContent)
            self.__currentArticle.details.supplierAltId = self.__currentContent
        
    def addDeliveryTime(self, attrs = None):
        if self.__currentArticle is None:
            raise Exception("Lieferzeit soll gespeichert werden. Aber es ist kein Artikel vorhanden")
        self.__currentArticle.addDeliveryTime(self.__currentContent)

    ''' ---------------------------------------------------------------------'''
    def __convertToEnglishDecimalValue(self, stringValue):
        convertedString = stringValue
        if not self.__decimalSeparator == ".": 
            convertedString = convertedString.replace(",",";").replace(self.__thousandSeparator,"").replace(";",".")
        logging.debug("'{0}'".format(convertedString))
        if convertedString is not None and len(convertedString) > 0 :
            return float(convertedString)
        else:
            return 0


    ''' ---------------------------------------------------------------------'''

    def addPriceAmount(self, attrs = None):
        self.__currentPrice.amount = round(self.__convertToEnglishDecimalValue(self.__currentContent), 2)

    def addPriceCurrency(self, attrs = None):
        self.__currentPrice.currency = self.__currentContent

    def addPriceTax(self, attrs = None):
        stringValue = self.__currentContent.replace("%", "").strip()
        convertedValue = self.__convertToEnglishDecimalValue(stringValue)
        if convertedValue > 1:
            convertedValue = convertedValue / 100
        self.__currentPrice.tax = round(convertedValue, 2)

    def addPriceFactor(self, attrs = None):
        self.__currentPrice.factor = self.__convertToEnglishDecimalValue(self.__currentContent)
    
    def addPriceLowerBound(self, attrs = None):
        self.__currentPrice.lowerBound = self.__currentContent
        
    ''' ---------------------------------------------------------------------'''
    
    def addTerritory(self, attrs = None):
        if self.__currentElement is None:
            logging.warning("Territory kann nicht gespeichert werden.")
        else:
            self.__currentElement.territory = self.__currentContent

    ''' ---------------------------------------------------------------------'''
    def addMimeSource(self, attrs = None):
        self.__currentMime.source = self.__currentContent

    def addMimeType(self, attrs = None):
        self.__currentMime.mimeType = self.__currentContent

    def addMimeAlt(self, attrs = None):
        self.__currentMime.altenativeContent = self.__currentContent

    def addMimePurpose(self, attrs = None):
        self.__currentMime.purpose = self.__currentContent

    def addMimeDescription(self, attrs = None):
        self.__currentMime.description = self.__currentContent

    def addMimeOrder(self, attrs = None):
        self.__currentMime.order = self.__currentContent
    
    ''' ---------------------------------------------------------------------'''
    def addOrderUnit(self, attrs = None):
        self.__currentArticle.orderDetails.orderUnit = self.__currentContent
    
    def addContentUnit(self, attrs = None):
        self.__currentArticle.orderDetails.contentUnit = self.__currentContent

    def addPriceQuantity(self, attrs = None):
        self.__currentArticle.orderDetails.priceQuantity = self.__currentContent
        
    def addPackagingQuantity(self, attrs = None):
        self.__currentArticle.orderDetails.packingQuantity = self.__currentContent

    def addQuantityInterval(self, attrs = None):
        self.__currentArticle.orderDetails.quantityInterval = self.__currentContent

    def addQuantityMin(self, attrs = None):
        self.__currentArticle.orderDetails.quantityMin = self.__currentContent
        
    ''' ---------------------------------------------------------------------'''
    def addFeatureValue(self, attrs = None):
        if self.__currentFeature.variants is not None and len(self.__currentFeature.variants) > 0:
            raise Exception("Fehler im BMEcat: FeatureValue soll hinzugefuegt werden, es existieren aber schon FeatureVariants.")        
        self.__currentElement.addValue(self.__currentContent)

    def addFeatureUnit(self, attrs = None):
        if self.__currentFeature.unit is not None:
            raise Exception("Fehler im BMEcat: FeatureUnit soll gesetzt werden existiert aber schon.")
        self.__currentFeature.unit = self.getUnit(self.__currentContent)
            
    def getUnit(self, value):
        currentUnit = None
        if self.__bmecatUnitMapper.hasKey(value):
            currentUnit = self.__bmecatUnitMapper.getSIUnit(value)
        elif self.__etimUnitMapper.hasKey(value):
            currentUnit = self.__etimUnitMapper.getSIUnit(value)
        else:
            currentUnit = value
        return currentUnit 
        
    def addFeatureName(self, attrs = None):
        if self.__currentFeature.name is not None:
            raise Exception("Fehler im BMEcat: FeatureName soll gesetzt werden existiert aber schon.")
        self.__currentFeature.name = self.__currentContent

    def addFeatureDescription(self, attrs = None):
        if self.__currentFeature.description is not None:
            raise Exception("Fehler im BMEcat: FeatureDescription soll gesetzt werden existiert aber schon.")
        self.__currentFeature.description = self.__currentContent

    def addFeatureValueDetails(self, attrs = None):
        if self.__currentFeature.valueDetails is not None:
            raise Exception("Fehler im BMEcat: FeatureValueDetails sollen gesetzt werden existieren aber schon.")
        self.__currentFeature.valueDetails = self.__currentContent

    ''' -------------- '''
    def createFeatureVariantSet(self, attrs = None):
        if self.__currentFeature.values is not None and len(self.__currentFeature.values) > 0:
            raise Exception("Fehler im BMEcat: FeatureVariants sollen hinzugefuegt werden, es existieren aber schon FeatureValues.")
        if self.__currentFeature.variants is not None:
            raise Exception("Fehler im BMEcat: FeatureVariants sollen hinzugefuegt werden, es existieren aber schon FeatureVariants.")
        self.__currentFeature.variants = VariantSet()

    def addFeatureVariantSetOrder(self, attrs = None):
        if self.__currentFeature.variants is None:
            raise Exception("Fehler im BMEcat: FeatureVariantSetOrder soll gesetzt werden, aber es existiert noch kein VariantSet.")
        self.__currentFeature.addVariantOrder(int(self.__currentContent))

    def createFeatureVariant(self, attrs = None):
        if self.__currentFeature.values is not None and len(self.__currentFeature.values) > 0:
            raise Exception("Fehler im BMEcat: FeatureVariants sollen hinzugefuegt werden, es existieren aber schon FeatureValues.")
        if self.__currentFeature.variants is None:
            raise Exception("Fehler im BMEcat: FeatureVariant soll erstellt werden, aber es existiert noch kein VariantSet.")
        if self.__currentVariant is None:
            raise Exception("Fehler im BMEcat: FeatureVariant soll erstellt werden, aber es existiert schon eine.")
        self.__currentVariant = Variant()
        self.__currentElement = self.__currentVariant
        
    def addFeatureVariantProductIdSuffix(self, attrs = None):
        if self.__currentVariant is None:
            raise Exception("Fehler im BMEcat: FeatureVariantProductIdSuffix soll gesetzt werden, aber es existiert noch keine Variante.")
        self.__currentVariant.productIdSuffix = self.__currentContent

    def saveFeatureVariant(self, attrs = None):
        if self.__currentArticle.variants is None:
            raise Exception("Fehler im BMEcat: FeatureVariant soll gespeichert werden, aber es existiert kein VariantSet mehr.")
        self.__currentFeature.addVariant(self.__currentVariant)
        self.__currentVariant = None
        self.__currentElement = None
           
    ''' ---------------------------------------------------------------------'''
    def startDateTime(self, attrs = None):
        if attrs is None or not 'type' in attrs.getNames():
            logging.warning("DateTime kann nicht gespeichert werden.")
        else:
            self.__dateType = attrs.getValue('type')
            self.__currentElement = self.__currentPriceDetails
    
    def endDateTime(self, attrs = None):
        self.__dateType = None
        self.__currentElement = None
    
    def addDate(self, attrs = None):
        if self.__dateType is None:
            logging.warning("Datum kann nicht gespeichert werden.")
        elif self.__currentElement is None:
            logging.warning("Datum [" + self.__dateType + "] kann nicht gespeichert werden, weil kein Element zum Speichern existiert.")
        else:
            if self.__dateType == 'valid_start_date':
                logging.debug("Datum [" + self.__currentContent + "] wird als Startdatum gespeichert.")
                self.__currentElement.validFrom = datetime.strptime(self.__currentContent, self.__dateFormat)
            elif self.__dateType == 'valid_end_date':
                logging.debug("Datum [" + self.__currentContent + "] wird als Enddatum gespeichert.")
                self.__currentElement.validTo = datetime.strptime(self.__currentContent, self.__dateFormat)
            else:
                logging.warning("Datum [" + self.__dateType + "] kann nicht gespeichert werden.")

        
    ''' ---------------------------------------------------------------------'''
    def addKeyword(self, attrs = None):
        if self.__currentArticle is not None:
            self.__currentArticle.addKeyword(self.__currentContent)
            
    ''' ---------------------------------------------------------------------'''
    def valueIsNone(self, value, message=None, outputLevel=logging.WARN):
        if value is None:
            logging.log(outputLevel, message)
            return True 
        return False
        
    def valueIsNoneOrNotInlist(self, value, inList, message=None, outputLevel=logging.WARN):
        if self.valueIsNone(value, message, outputLevel):
            return True
        if value not in inList:
            logging.log(outputLevel, message)
            return True
        return False
        
    '''aktuellen Inhalt des XML-Elements ermitteln'''
    def characters(self, content):
        logging.debug("Original input: '{0}'".format(content))
        if self.__lineFeedToHTML:
            self.__currentContent += content.replace("\n","<br>").strip()
        else:
            if len(self.__currentContent) > 0 and len(content) > len(content.strip()):
                self.__currentContent = self.__currentContent.strip() + ' '
            self.__currentContent += content.strip()
        logging.debug("Saved input: '{0}'".format(self.__currentContent))

    def validateCurrentProduct(self):
        if self.__currentArticle is None:
            raise Exception("Es wurde kein aktuell zu bearbeitender Artikel gefunden.")
        self.__currentArticle.validate()