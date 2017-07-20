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

class ExcelImporter(object):
    
    basefieldMapping = {
        # Produktrumpf
        "supplierArticleId" : "productId"
    }
    
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
    
    orderDetailMapping = {
        # Order Details
        "orderUnit" : "orderUnit",
        "contentUnit" : "contentUnit",
        "packingQuantity" : "packingQuantity",
        "priceQuantity" : "priceQuantity",
        "quantityMin" : "quantityMin",
        "quantityInterval" : "quantityInterval"
    }
    
    featureMapping = { "attributeName" : "name", "attributeValue" : "value" }
    
    priceMapping = {
        "priceType" : "priceType",
        "priceAmount" : "amount",
        "tax" : "tax",
        "lowerBound" : "lowerBound",
        "factor" : "factor",
        "territory" : "territory",
        "currency" : "currency"
        }

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
        for colIndex in range(1,sheet.max_column):
            currentFieldname = sheet.cell(column=colIndex, row=1).value
            if currentFieldname is not None and currentFieldname.strip() is not None and len(currentFieldname.strip()) > 0:
                print (currentFieldname)
                if currentFieldname in self.basefieldMapping.keys():
                    self.indexForProduct[colIndex] = self.basefieldMapping[currentFieldname]
                elif currentFieldname in self.productDetailMapping.keys():
                    self.indexForProductDetails[colIndex] = self.productDetailMapping[currentFieldname]
                elif currentFieldname in self.orderDetailMapping.keys():
                    self.indexForOrderDetails[colIndex] = self.orderDetailMapping[currentFieldname]                
                else:
                    firstPart = regex.match("[a-zA-Z]*", currentFieldname).group(0)
                    secondPart = currentFieldname.replace(firstPart, "")
                    
                    print("'{0}' : '{1}'".format(firstPart, secondPart)) #logging.debug
                    
                    columnNameToClassFieldName = None
                    indexForClassFieldName = None
                    
                    if firstPart in self.priceMapping.keys():
                        indexForClassFieldName = self.indexTuplesForPrices
                        columnNameToClassFieldName = self.priceMapping
                    elif firstPart in self.mimeMapping.keys():
                        indexForClassFieldName = self.indexTuplesForMimes
                        columnNameToClassFieldName = self.mimeMapping
                    elif firstPart in self.featureMapping.keys():
                        indexForClassFieldName = self.indexPairsForFeatures
                        columnNameToClassFieldName = self.featureMapping
                    else:
                        logging.debug("'{0}' : '{1}'".format(firstPart, secondPart))
                        continue
                        
                    if secondPart not in indexForClassFieldName.keys():
                        indexForClassFieldName[secondPart] = { columnNameToClassFieldName[firstPart] : colIndex } 
                    else:
                        indexForClassFieldName[secondPart][columnNameToClassFieldName[firstPart]] = colIndex
