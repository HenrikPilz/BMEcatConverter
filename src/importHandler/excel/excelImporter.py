'''
Created on 11.05.2017

@author: henrik.pilz
'''

import logging
import copy
import regex
from openpyxl import load_workbook
from multiprocessing.connection import arbitrary_address
from inspect import currentframe
from data.product import Product
from data.productDetails import ProductDetails
from data.orderDetails import OrderDetails

class ExcelImporter(object):
    # Grunddaten eines Artikels. Mindestens die Artikelnummer
    basefieldMapping = {
        # Produktrumpf
        "supplierArticleId" : "productId"
    }
    
    # Artiekldetails
    productDetailMapping = {
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
    orderDetailMapping = {
        # Order Details
        "orderUnit" : "orderUnit",
        "contentUnit" : "contentUnit",
        "packingQuantity" : "packingQuantity",
        "priceQuantity" : "priceQuantity",
        "quantityMin" : "quantityMin",
        "quantityInterval" : "quantityInterval"
    }
    
    # technische Daten
    featureMapping = { "attributeName" : "name", "attributeValue" : "value" }
    
    # Preisdaten
    priceMapping = {
        "priceType" : "priceType",
        "priceAmount" : "amount",
        "tax" : "tax",
        "lowerBound" : "lowerBound",
        "factor" : "factor",
        "territory" : "territory",
        "currency" : "currency"
        }

    # Bilddaten
    mimeMapping = {
        "mimeType" : "mimeType",
        "mimeSource" : "source",
        "mimeDescription" : "description",
        "mimeAlt" : "altenativeContent",
        "mimePurpose" : "purpose",
        "mimeOrder" : "order"
        }

    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.indexForProduct = {}
        self.indexForProductDetails = {}
        self.indexForOrderDetails = {}
        self.indexPairsForFeatures = {}
        self.indexTuplesForPrices = {}
        self.indexTuplesForMimes = {}
        
    def readWorkbook(self, filename, tablename):
        wb = load_workbook(filename)
        articleSheet =  wb[tablename]
        
        self.determineIndexMappings(articleSheet)
        
    def determineIndexMappings(self, sheet):
        # gehe durch alle Spalten in Zeile 1 (Headerzeile)
        for colIndex in range(1,sheet.max_column):        
            # hole den aktuellen Feldnamen    
            currentFieldname = sheet.cell(column=colIndex, row=1).value
            # wenn der Feldnam nicht leer ist
            if currentFieldname is not None and currentFieldname.strip() is not None and len(currentFieldname.strip()) > 0:
                # gib ihn aus
                print (currentFieldname)
                # ist er in den basefieldKeys (Grunddatenfelder des Artikels)
                if currentFieldname in self.basefieldMapping.keys():
                    self.indexForProduct[self.basefieldMapping[currentFieldname]] = colIndex
                # ist er product detail relevant
                elif currentFieldname in self.productDetailMapping.keys():                    
                    self.indexForProductDetails[self.productDetailMapping[currentFieldname]] = colIndex
                # bestelldetails
                elif currentFieldname in self.orderDetailMapping.keys():
                    self.indexForOrderDetails[self.orderDetailMapping[currentFieldname]] = colIndex
                # andere Daten?                
                else:
                    # dann muessen wir splitten, da der Zahlenanteil
                    # Sowohl die Zusammengehörigkeit der Daten anzeigt,
                    # als auch die Reihenfolge bestimmt
                    fieldName = regex.match("[a-zA-Z]*", currentFieldname).group(0)
                    fieldCount = currentFieldname.replace(fieldName, "")
                    
                    print("'{0}' : '{1}'".format(fieldName, fieldCount)) #logging.debug
                    
                    columnNameToClassFieldName = None
                    indexForClassFieldName = None
                    
                    # sind es preisdetails ?
                    if fieldName in self.priceMapping.keys():
                        indexForClassFieldName = self.indexTuplesForPrices
                        columnNameToClassFieldName = self.priceMapping
                    elif fieldName in self.mimeMapping.keys():
                        indexForClassFieldName = self.indexTuplesForMimes
                        columnNameToClassFieldName = self.mimeMapping
                    elif fieldName in self.featureMapping.keys():
                        indexForClassFieldName = self.indexPairsForFeatures
                        columnNameToClassFieldName = self.featureMapping
                    else:
                        logging.debug("'{0}' : '{1}'".format(columnNameToClassFieldName[fieldName], fieldCount))
                        continue

                    classFieldName = columnNameToClassFieldName[fieldName]                        
                    if classFieldName not in indexForClassFieldName.keys():
                        indexForClassFieldName[classFieldName] = { fieldCount : colIndex } 
                    else:
                        indexForClassFieldName[classFieldName][fieldCount] = colIndex

    def readArticles(self, sheet):
        for rowIndex in range(2, sheet.max_row):
            currentProduct = Product()
            self.addInformationForMapping(self.indexForProduct, currentProduct, rowIndex, sheet)
            currentProduct.details = ProductDetails()
            self.addInformationForMapping(self.indexForProductDetails, currentProduct.details, rowIndex, sheet)
            currentProduct.orderDetails = OrderDetails()
            self.addInformationForMapping(self.indexForOrderDetails, currentProduct.orderDetails, rowIndex, sheet)
            

    def addInformationForMapping(self, mapping, objectForValue, rowIndex, sheet):
        for fieldname in mapping.keys():
            setattr(objectForValue, fieldname, sheet.cell(columnIndex=mapping[fieldname], row=rowIndex))