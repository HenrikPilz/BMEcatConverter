'''
Created on 11.05.2017

@author: henrik.pilz
'''

import logging

from openpyxl import load_workbook
import regex

from datamodel import FeatureSet, Mime, OrderDetails, PriceDetails, Product, ProductDetails, Price, Feature
from transformer.Separators import SeparatorTransformer


class ExcelImporter(object):
    '''
    classdocs
    '''

    # Namen der mögliche Tabellen mit Artikeln
    __allowedTablenames = [ 'Artikel', 'Tabelle1', 'Mapping-Master' ]

    # Grunddaten eines Artikels. Mindestens die Artikelnummer
    __basefieldMapping = {
        # Produktrumpf
        "supplierArticleId" : "productId"
    }

    # Artikeldetails
    __productDetailMapping = {
        # Produktdetails
        "descriptionShort" : "title",
        "descriptionLong" : "description",
        "ean" : "ean",
        "supplierAltId" : "supplierAltId",
        "buyerId" : "buyerId",
        "manufacturerArticleId" : "manufacturerArticleId",
        "manufacturerName" : "manufacturerName",
        "deliveryTime" : "deliveryTime"
    }

    # Bestelldetails
    __orderDetailMapping = {
        # Order Details
        "orderUnit" : "orderUnit",
        "contentUnit" : "contentUnit",
        "ContentUnit" : "contentUnit",
        "packingQuantity" : "packingQuantity",
        "priceQuantity" : "priceQuantity",
        "quantityMin" : "quantityMin",
        "quantityInterval" : "quantityInterval"
    }

    # technische Daten
    __featureMapping = {
        "attribute_name" : "name",
        "attributeName" : "name",
        "attribute_value" : "values",
        "attributeValue" : "values",
        "attribute_unit" : "unit",
        "attributeUnit" : "unit"
    }

    # Preisdaten
    __priceMapping = {
        "priceType" : "priceType",
        "price_type" : "priceType",
        "priceAmount" : "amount",
        "price_amount" : "amount",
        "tax" : "tax",
        "lowerBound" : "lowerBound",
        "lower_bound" : "lowerBound",
        "factor" : "factor",
        "territory" : "territory",
        "currency" : "currency"
    }

    # Bilddaten
    __mimeMapping = {
        "mimeType" : "mimeType",
        "mime_type" : "mimeType",
        "mimeSource" : "source",
        "mime_source" : "source",
        "mimeDescription" : "description",
        "mime_description" : "description",
        "mimeAlt" : "altenativeContent",
        "mime_alt" : "altenativeContent",
        "mimePurpose" : "purpose",
        "mime_purpose" : "purpose",
        "mimeOrder" : "order",
        "mime_order" : "order"
    }

    __fieldsToTransform = [ "amount", "tax", "factor" ]

    def __init__(self, separatorTransformer=SeparatorTransformer("detect")):
        '''
        Constructor
        '''
        self.__indexForProduct = {}
        self.__indexForProductDetails = {}
        self.__indexForOrderDetails = {}
        self.__indexPairsForFeatures = {}
        self.__indexTuplesForPrices = {}
        self.__indexTuplesForMimes = {}
        self._separatorTransformer = separatorTransformer

        self.articles = []

    def readWorkbook(self, filename):
        wb = load_workbook(filename)
        countPossibleCandidates = 0
        tablename = None
        for allowedSheetname in self.__allowedTablenames:
            if allowedSheetname in wb.sheetnames:
                countPossibleCandidates += 1
                tablename = allowedSheetname

        if tablename is None:
            raise Exception("Das Tabellenblatt mit den Artikelnamen sollte einen der folgenden Namen tragen: '{0}'".format(", ".join(self.__allowedTablenames)))
        if countPossibleCandidates > 1:
            raise Exception("Es darf nur ein Tabellenblatt mit den folgenden Artikelnamen existieren: '{0}'".format(", ".join(self.__allowedTablenames)))

        articleSheet = wb[tablename]
        self.__determineIndexMappings(articleSheet)
        self.__readArticles(articleSheet)

    def __determineIndexMappings(self, sheet):
        # gehe durch alle Spalten in Zeile 1 (Headerzeile)
        for colIndex in range(1, sheet.max_column + 1):
            # hole den aktuellen Feldnamen
            currentFieldname = sheet.cell(column=colIndex, row=1).value
            # wenn der Feldnam nicht leer ist
            if currentFieldname is not None and currentFieldname.strip() is not None and len(currentFieldname.strip()) > 0:
                # gib ihn aus
                logging.debug(currentFieldname)
                # ist er in den basefieldKeys (Grunddatenfelder des Artikels)
                if currentFieldname in self.__basefieldMapping.keys():
                    self.__indexForProduct[self.__basefieldMapping[currentFieldname]] = colIndex
                # ist er product detail relevant
                elif currentFieldname in self.__productDetailMapping.keys():
                    self.__indexForProductDetails[self.__productDetailMapping[currentFieldname]] = colIndex
                # bestelldetails
                elif currentFieldname in self.__orderDetailMapping.keys():
                    self.__indexForOrderDetails[self.__orderDetailMapping[currentFieldname]] = colIndex
                # andere Daten?
                else:
                    # dann muessen wir splitten, da der Zahlenanteil
                    # Sowohl die Zusammengehörigkeit der Daten anzeigt,
                    # als auch die Reihenfolge bestimmt
                    fieldName = regex.match("[a-zA-Z_]*", currentFieldname).group(0)
                    fieldName = fieldName.strip("_")
                    fieldCount = currentFieldname.replace(fieldName, "").strip("_")

                    logging.debug("'{0}' : '{1}'".format(fieldName, fieldCount))

                    columnNameToClassFieldName = None
                    indexForClassFieldName = None

                    # sind es preisdetails ?
                    if fieldName in self.__priceMapping.keys():
                        indexForClassFieldName = self.__indexTuplesForPrices
                        columnNameToClassFieldName = self.__priceMapping
                    elif fieldName in self.__mimeMapping.keys():
                        indexForClassFieldName = self.__indexTuplesForMimes
                        columnNameToClassFieldName = self.__mimeMapping
                    elif fieldName in self.__featureMapping.keys():
                        indexForClassFieldName = self.__indexPairsForFeatures
                        columnNameToClassFieldName = self.__featureMapping
                    else:
                        logging.debug("'{0}' : '{1}'".format(fieldName, fieldCount))
                        continue

                    classFieldName = columnNameToClassFieldName[fieldName]
                    if classFieldName not in indexForClassFieldName.keys():
                        indexForClassFieldName[classFieldName] = { fieldCount : colIndex }
                    else:
                        indexForClassFieldName[classFieldName][fieldCount] = colIndex

    def __readArticles(self, sheet):
        for rowIndex in range(2, sheet.max_row + 1):
            currentProduct = self.__createProduct(sheet, rowIndex)
            self.articles.append(currentProduct)

    def __createProduct(self, sheet, rowIndex):
        currentProduct = Product()
        self.__transferInformationForMapping(self.__indexForProduct, currentProduct, rowIndex, sheet)
        currentProduct.details = ProductDetails()
        self.__transferInformationForMapping(self.__indexForProductDetails, currentProduct.details, rowIndex, sheet)
        currentProduct.orderDetails = OrderDetails()
        self.__transferInformationForMapping(self.__indexForOrderDetails, currentProduct.orderDetails, rowIndex, sheet)
        self.__addMultipleOrderedObjects(self.__indexTuplesForMimes, currentProduct, Mime, rowIndex, sheet)
        priceDetails = PriceDetails()
        self.__addMultipleOrderedObjects(self.__indexTuplesForPrices, priceDetails, Price, rowIndex, sheet)
        currentProduct.addPriceDetails(priceDetails)
        featureSet = FeatureSet()
        self.__addMultipleOrderedObjects(self.__indexPairsForFeatures, featureSet, Feature, rowIndex, sheet)
        currentProduct.addFeatureSet(featureSet)
        return currentProduct

    def __addMultipleOrderedObjects(self, mapping, objectContainer, typeOfMultiples, rowIndex, sheet):
        """
        Fügt mehrere Objekte zum Objektcontainer hinzu
        """
        itemsToAddByOrder = {}
        for fieldname in mapping.keys():
            for order, colIndex in mapping[fieldname].items():
                if order not in itemsToAddByOrder.keys():
                    itemsToAddByOrder[order] = typeOfMultiples()
                value = sheet.cell(column=colIndex, row=rowIndex).value
                if fieldname in self.__fieldsToTransform:
                    value = self._separatorTransformer.transform(value)
                itemsToAddByOrder[order].add(fieldname, value)

        for key in sorted(itemsToAddByOrder.keys()):
            try:
                if getattr(itemsToAddByOrder[key], "order") is None:
                    setattr(itemsToAddByOrder[key], "order", int(key))
            except AttributeError:
                pass
            self.__exectueAddMethod(objectContainer, "add" + str(typeOfMultiples.__name__), itemsToAddByOrder[key])

    def __transferInformationForMapping(self, mapping, objectForValue, rowIndex, sheet):
        """
        Überträgt die Informationen vom Objekt über das angegebene Mapping für das Produkt in der Zeile.
        """
        for fieldname in mapping.keys():
            value = sheet.cell(column=mapping[fieldname], row=rowIndex).value
            if fieldname in self.__fieldsToTransform:
                value = self._separatorTransformer.transform(value)
            setattr(objectForValue, fieldname, value)

    def __exectueAddMethod(self, objectWithAddMethod , addMethodName, arg):
        elementHandler = None
        try:
            if addMethodName is not None:
                elementHandler = getattr(objectWithAddMethod, addMethodName)
                elementHandler(arg)
            self.__currentContent = ""
        except AttributeError:
            raise NotImplementedError("Class [" + objectWithAddMethod.__class__.__name__ + "] does not implement [" + addMethodName + "]")
