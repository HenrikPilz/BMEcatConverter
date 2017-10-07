'''
Created on 05.05.2017

@author: henrik.pilz
'''
import copy
import logging

from openpyxl.workbook import Workbook


class PyxelHandler(object):
    '''
    classdocs
    '''


    def __init__(self, articles, filename, defaultManufacturerName=None):
        '''
        Constructor
        '''
        self._defaultManufacturerName = defaultManufacturerName
        self._headerRowIndex = 1
        self._filename = filename
        self._articles = copy.deepcopy(articles)
        self._firstPriceColumIndex = -1
        self._firstAttributeColumIndex = -1
        self._firstMimeColumIndex = -1
        self._firstSpecialTreatmentColumIndex = -1

        ''' Anzahl Preise, Attribute, Bilder, TreatmentClasses, Artikel'''
        self._maxNumberOfPrices = 0
        self._maxNumberOfAttributes = 0
        self._maxNumberOfMimes = 0
        self._maxNumberOfSpecialTreatmentClasses = 0
        self._numberOfArticlesProcessed = 0

        for articles in self._articles.values():
            for article in articles:
                numberOfVariants = None
                numberOfPrices = 0
                for priceDetailEntry in article.priceDetails:
                    numberOfPrices += len(priceDetailEntry.prices)
                self._maxNumberOfPrices = max(numberOfPrices, self._maxNumberOfPrices)
                numberOfAttributes = 0
                for featureSet in article.featureSets:                
                    numberOfAttributes += len(featureSet.features)
                    for feature in featureSet.features:
                        if feature.variants is not None:
                            numberOfVariants = numberOfVariants * len(feature.variants)
                if numberOfVariants is None:
                    self._numberOfArticlesProcessed += 1
                else:
                    self._numberOfArticlesProcessed += numberOfVariants
                    article.numberOfVariants = numberOfVariants
                 
                self._maxNumberOfAttributes = max(numberOfAttributes, self._maxNumberOfAttributes)
                self._maxNumberOfMimes = max(len(article.mimeInfo), self._maxNumberOfMimes)
                self._maxNumberOfSpecialTreatmentClasses = max(len(article.details.specialTreatmentClasses), self._maxNumberOfSpecialTreatmentClasses)

    def createNewWorkbook(self):
        wb = Workbook()
        self.createArtikelSheet(wb)
        wb.save(self._filename)
        self.createReferencesSheet(wb)
        wb.save(self._filename)        
        self.createKeywordsSheet(wb)
        wb.save(self._filename)

    def createArtikelSheet(self, wb):
        logging.info("Übertrage Artikel.")
        sheet = wb.create_sheet("Artikel", 0)
        self.createArtikelHeader(sheet)
        self.writeArticlesToSheet(sheet)

    def createArtikelHeader(self, sheet):
        columnIndex = 1

        baseFields = [ "articleType", "articleId", "supplierArticleId",
                       "descriptionShort", "descriptionLong", "ean",
                       "manufacturerArticleId", "manufacturerName",
                       "deliveryTime", "orderUnit",
                       "contentUnit", "packingQuantity", "priceQuantity",
                       "quantityMin", "quantityInterval" ]
        priceFields = [ "validFrom", "validTo", "priceType", "priceAmount",
                        "priceCurrency", "tax", "priceFactor", "lowerBound" ]
        mimeFields = [ "mimeType", "mimeSource", "mimeAlt", "mimeDescription",
                       "mimePurpose", "mimeOrder" ]
        attributeFields = [ "attributeName", "attributeValue" ] 
        ''', "attributeUnit" ]'''
        treatmentClassFields = [ "classType", "className" ]

        for fieldName in baseFields:
            sheet.cell(row=self._headerRowIndex, column=columnIndex, value=fieldName)
            columnIndex+=1

        logging.info( "Anzahl verarbeiteter Artikel: " + str(self._numberOfArticlesProcessed))
        logging.info( "Maximale Anzahl Preise: " + str(self._maxNumberOfPrices))
        logging.info( "Maximale Anzahl Bilder: " + str(self._maxNumberOfMimes))
        logging.info( "Maximale Anzahl Attribute: " + str(self._maxNumberOfAttributes))
        logging.info( "Maximale Anzahl Spezialbehandlungsklassen: " + str(self._maxNumberOfSpecialTreatmentClasses))


        if self._maxNumberOfPrices > 0:
            self._firstPriceColumIndex = columnIndex
            for p in range(1, self._maxNumberOfPrices+1):
                for fieldName in priceFields:
                    sheet.cell(row=self._headerRowIndex, column=columnIndex, value=fieldName + str(p))
                    columnIndex+=1

        if self._maxNumberOfMimes> 0:
            self._firstMimeColumIndex = columnIndex
            for m in range(1, self._maxNumberOfMimes+1):
                for fieldName in mimeFields:
                    sheet.cell(row=self._headerRowIndex, column=columnIndex, value=fieldName + str(m))
                    columnIndex+=1

        if self._maxNumberOfAttributes > 0:
            self._firstAttributeColumIndex = columnIndex
            for a in range(1, self._maxNumberOfAttributes+1):
                for fieldName in attributeFields:
                    sheet.cell(row=self._headerRowIndex, column=columnIndex, value=fieldName + str(a))
                    columnIndex+=1

        if self._maxNumberOfSpecialTreatmentClasses > 0:
            self._firstSpecialTreatmentColumIndex = columnIndex
            for s in range(1, self._maxNumberOfSpecialTreatmentClasses+1):
                for fieldName in treatmentClassFields:
                    sheet.cell(row=self._headerRowIndex, column=columnIndex, value=fieldName + str(s))
                    columnIndex+=1

    def writeArticlesToSheet(self, sheet):
        rowIndex = self._headerRowIndex + 1
        for articleType in self._articles.keys():
            for article in self._articles[articleType]:
                self.writeOneArticleToRow(articleType, article, rowIndex, sheet)
                rowIndex += 1

    def writeOneArticleToRow(self, articleType, article, rowIndex, sheet):
        self.addBaseFieldsToArticle(articleType, article, rowIndex, sheet)
        self.addMimesToArticle(article.mimeInfo, rowIndex, sheet)
        self.addPricesToArticle(article.priceDetails, rowIndex, sheet)
        self.addAttributesToArticle(article.featureSets, rowIndex, sheet)
        self.addTreatmentClassesToArticle(article.details.specialTreatmentClasses, rowIndex, sheet)


    def addBaseFieldsToArticle(self, articleType, article, rowIndex, sheet):
        columnIndex = 1
        sheet.cell(row=rowIndex, column=columnIndex, value=articleType)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value="")
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.productId.strip().replace(" ",""))
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.details.title)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.details.description)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.details.ean)
        columnIndex += 1
        if article.details.manufacturerArticleId is None:
            sheet.cell(row=rowIndex, column=columnIndex, value=article.productId.strip())
        else:
            sheet.cell(row=rowIndex, column=columnIndex, value=article.details.manufacturerArticleId.strip())
        columnIndex += 1
        if article.details.manufacturerName is None:
            sheet.cell(row=rowIndex, column=columnIndex, value=self._defaultManufacturerName)
        else:
            sheet.cell(row=rowIndex, column=columnIndex, value=article.details.manufacturerName)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.details.deliveryTime)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.orderDetails.orderUnit)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.orderDetails.contentUnit)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.orderDetails.packingQuantity)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.orderDetails.priceQuantity)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.orderDetails.quantityMin)
        columnIndex += 1
        sheet.cell(row=rowIndex, column=columnIndex, value=article.orderDetails.quantityInterval)

    def addPricesToArticle(self, priceDetails, rowIndex, sheet):
        if self._firstPriceColumIndex < 1:
            logging.warning("Keine Preise zu transferieren.")
            return
        priceCount = 0
        fieldCount = 8
        for priceDetail in priceDetails:
            for price in priceDetail.prices:
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount, value=priceDetail.validFrom)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 1, value=priceDetail.validTo)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 2, value=price.priceType)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 3, value=price.amount)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 4, value=price.currency)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 5, value=price.tax)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 6, value=price.factor)
                sheet.cell(row=rowIndex, column=self._firstPriceColumIndex + priceCount*fieldCount + 7, value=price.lowerBound)
                priceCount += 1

    def addMimesToArticle(self, mimeInfo, rowIndex, sheet):
        if self._firstMimeColumIndex < 1:
            logging.info("Keine Bilder zu transferieren.")
            return
        mimeCount = 0
        fieldCount = 6
        for mime in mimeInfo:
            sheet.cell(row=rowIndex, column=self._firstMimeColumIndex + mimeCount*fieldCount, value=mime.mimeType)
            sheet.cell(row=rowIndex, column=self._firstMimeColumIndex + mimeCount*fieldCount + 1, value=mime.source)
            sheet.cell(row=rowIndex, column=self._firstMimeColumIndex + mimeCount*fieldCount + 2, value=mime.altenativeContent)
            sheet.cell(row=rowIndex, column=self._firstMimeColumIndex + mimeCount*fieldCount + 3, value=mime.description)
            sheet.cell(row=rowIndex, column=self._firstMimeColumIndex + mimeCount*fieldCount + 4, value=mime.purpose)
            sheet.cell(row=rowIndex, column=self._firstMimeColumIndex + mimeCount*fieldCount + 5, value=mime.order)
            mimeCount += 1

    def addAttributesToArticle(self, featureSets, rowIndex, sheet, currentVariant=None):
        if self._firstAttributeColumIndex < 1:
            logging.info("Keine Attribute zu transferieren.")
            return
        attributeCount = 0
        fieldCount = 2
        for featureSet in featureSets:
            for feature in featureSet.features:
                sheet.cell(row=rowIndex, column=self._firstAttributeColumIndex + attributeCount*fieldCount, value=feature.name)

                cellValue = None
                for value in feature.values:
                    if cellValue is None:
                        cellValue = value
                    else:
                        cellValue += " | "
                        cellValue += value 
                    
                    if not feature.unit is None and not feature.unit.strip() == "":
                        cellValue += " " + feature.unit

                sheet.cell(row=rowIndex, column=self._firstAttributeColumIndex + attributeCount*fieldCount + 1, value=cellValue)
                attributeCount += 1

    def addTreatmentClassesToArticle(self, specialTreatmentClasses, rowIndex, sheet):
        if self._firstSpecialTreatmentColumIndex < 1:
            logging.info("Keine Fälle für Spezialbehandlungen zu transferieren.")
            return
        classCount = 0
        fieldCount = 2
        for treatmentClass in specialTreatmentClasses:
            sheet.cell(row=rowIndex, column=self._firstSpecialTreatmentColumIndex + classCount*fieldCount, value=treatmentClass.classType)
            sheet.cell(row=rowIndex, column=self._firstSpecialTreatmentColumIndex + classCount*fieldCount + 1, value=treatmentClass.value)
            classCount += 1

    def createReferencesSheet(self, wb):
        logging.info("Übertrage Artikelbeziehungen.")
        sheet = wb.create_sheet("Artikelbeziehungen", 1)
        self.createReferencesHeader(sheet)
        self.writeReferencesToSheet(sheet)

    def createReferencesHeader(self, sheet):
        columnIndex = 1
        sheet.cell(row=self._headerRowIndex, column=columnIndex, value="supplierArticleId")
        columnIndex += 1
        sheet.cell(row=self._headerRowIndex, column=columnIndex, value="referencType")
        columnIndex += 1
        sheet.cell(row=self._headerRowIndex, column=columnIndex, value="referencedSupplierArticleId")

    def writeReferencesToSheet(self, sheet):
        rowIndex = self._headerRowIndex + 1
        for articleType in self._articles.keys():
            for article in self._articles[articleType]:
                rowIndex += self.writeReferencesForOneArticle(article, rowIndex, sheet)

    def writeReferencesForOneArticle(self, article, rowIndex, sheet):
        count = 0
        for reference in article.references:
            for referencedArticleId in reference.supplierArticleIds:
                columnIndex = 1
                sheet.cell(row=rowIndex+count, column=columnIndex, value=article.productId)
                columnIndex += 1
                sheet.cell(row=rowIndex+count, column=columnIndex, value=reference.referenceType)
                columnIndex += 1
                sheet.cell(row=rowIndex+count, column=columnIndex, value=referencedArticleId)
                count += 1
        return count

    def createKeywordsSheet(self, wb):
        logging.info("Übertrage Artikelsuchbegriffe.")
        sheet = wb.create_sheet("Artikelsuchbegriffe", 1)
        self.createKeywordsHeader(sheet)
        self.writeKeywordsToSheet(sheet)

    def createKeywordsHeader(self, sheet):
        columnIndex = 1
        sheet.cell(row=self._headerRowIndex, column=columnIndex, value="supplierArticleId")
        columnIndex += 1
        sheet.cell(row=self._headerRowIndex, column=columnIndex, value="keywords")

    def writeKeywordsToSheet(self, sheet):
        rowIndex = self._headerRowIndex + 1
        for articleType in self._articles.keys():
            for article in self._articles[articleType]:
                if len(article.details.keywords) > 0:
                    rowIndex += self.writeKeywordsForOneArticle(article, rowIndex, sheet)

    def writeKeywordsForOneArticle(self, article, rowIndex, sheet):
        count = 0
        columnIndex = 1
        sheet.cell(row=rowIndex+count, column=columnIndex, value=article.productId)
        columnIndex += 1
        sheet.cell(row=rowIndex+count, column=columnIndex, value=",".join(['"{0}"'.format(keyword) for keyword in article.details.keywords]) )
        count += 1
        return count