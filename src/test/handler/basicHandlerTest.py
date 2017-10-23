'''
Created on 08.10.2017

@author: Henrik Pilz
'''
import unittest

from abc import abstractmethod


class BasicHandlerTest(unittest.TestCase):

    @abstractmethod
    def runTestMethod(self):
        '''
        @return array of articles 
        '''
        raise NotImplemented

    def runAndCheck(self, article, filename):        
        article.validate(True)
        article2 = self.runTestMethod(article, filename )[0]


        self.assertEqual(article.productId, article2.productId, "Artikelnummer")
        self.assertEqual(article.details.deliveryTime, int(article2.details.deliveryTime), "deliveryTime")
        self.assertEqual(article.details.ean, article2.details.ean, "ean")
        self.assertEqual(article.details.title, article2.details.title, "title")
        self.assertEqual(article.details.description, article2.details.description, "description")
        if article.details.manufacturerArticleId is None and article2.details.manufacturerArticleId is not None:
            self.assertEqual(article.productId, article2.details.manufacturerArticleId, "manufacturerArticleId")
        else:
            self.assertEqual(article.details.manufacturerArticleId, article2.details.manufacturerArticleId, "manufacturerArticleId")

        self.assertEqual(article.details.manufacturerName, article2.details.manufacturerName, "manufacturerName")
        
        if len(article.details.keywords) > 0 and len(article2.details.keywords) > 0:
            self.assertEqual(article.details.keywords, article2.details.keywords, "keywords")
        if len(article.details.specialTreatmentClasses) > 0 and len(article2.details.specialTreatmentClasses) > 0:
            self.assertEqual(article.details.specialTreatmentClasses, article2.details.specialTreatmentClasses, "specialTreatmentClasses")
            
        self.assertEqual(article.details.erpGroupBuyer, article2.details.erpGroupBuyer, "erpGroupBuyer")
        self.assertEqual(article.details.erpGroupSupplier, article2.details.erpGroupSupplier, "erpGroupSupplier")
        self.assertEqual(article.details.remarks, article2.details.remarks, "remarks")
        self.assertEqual(article.details.buyerId, article2.details.buyerId, "buyerId")
        self.assertEqual(article.details.segment, article2.details.segment, "segment")
        self.assertEqual(article.details.articleOrder, article2.details.articleOrder, "articleOrder")
        self.assertEqual(article.details.articleStatus, article2.details.articleStatus, "articleStatus")
        if article.details.supplierAltId is not None and article2.details.supplierAltId is not None:
            self.assertEqual(article.details.supplierAltId, article2.details.supplierAltId, "supplierAltId")
            
        self.assertEqual(article.details.manufacturerTypeDescription, article2.details.manufacturerTypeDescription, "manufacturerTypeDescription")

        self.assertEqual(article.orderDetails, article2.orderDetails, "orderDetails")
        self.assertEqual(len(article.featureSets), len(article2.featureSets), "lean(featureSets)")
        if len(article.featureSets) > 0:
            self.assertEqual(len(article.featureSets[0]), len(article2.featureSets[0]), "len(featureSets[0])")
            self.assertEqual(article.featureSets[0].referenceSytem, article2.featureSets[0].referenceSytem, "featureSets.referenceSytem")
            if len(article.featureSets[0].features) > 0:
                self.assertEqual(article.featureSets[0].features[0].name, article2.featureSets[0].features[0].name, "feature[0].name")
                self.assertEqual(article.featureSets[0].features[0], article2.featureSets[0].features[0], "feature[0]")
            
            self.assertEqual(article.featureSets[0], article2.featureSets[0], "featureSet[0]")
        self.assertEqual(article.featureSets, article2.featureSets, "featureSets")
        self.assertEqual(article.mimeInfo, article2.mimeInfo, "mimeInfo")
        if len(article.references) > 0 and len(article2.references) > 0 :
            self.assertEqual(article.references, article2.references, "references")        
    