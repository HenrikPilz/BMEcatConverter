'''
Created on 12.05.2017

@author: henrik.pilz
'''
from datetime import datetime
import getpass
import logging

from lxml import etree
from lxml.etree import Element, SubElement


class BMEcatExporter(object):
    
    def __init__(self, articles, filename, merchant='fiege'):
        self._articles = articles # dict!
        self._filename = filename
        self._merchant = merchant
    
    def __createArticleElements(self):
        articleElements = []
        for articleType, articles in self._articles.items():
            articleElements.extend(self.__createArticleElementsForSet(articles, articleType))
        return articleElements

    def __createArticleElementsForSet(self, articles, articleType='new'):
        articleElements = []
        for article in articles:
            articleElement = article.toXml(articleType)
            articleElements.append(articleElement)
        return articleElements
    
    def writeBMEcatAsXML(self):
        with open(self._filename, "wb") as file:
            bmecat = self.__createBMEcatRootElement()
            bmecat.append(self.__createHeaderElement())
            
            newCatalog = Element("T_NEW_CATALOG")
            newCatalog.append(self.__createCatalogGroupSystemElement())
            bmecat.append(newCatalog)    
            newCatalog.extend(self.__createArticleElements())
            newCatalog.extend(self.__createArticleCatalogMapping())
            file.write(self.__prettyFormattedOutput(bmecat))
            file.close()
        
    def __createBMEcatRootElement(self):
        return etree.XML('<!DOCTYPE BMECAT SYSTEM "bmecat_new_catalog.dtd">' +
                        '<BMECAT version="1.2" xml:lang="de" xmlns="http://www.bmecat.org/bmecat/1.2/bmecat_new_catalog" />')

    def __createCatalogGroupSystemElement(self):
        return etree.XML("<CATALOG_GROUP_SYSTEM>" +
                            "<GROUP_SYSTEM_ID>1</GROUP_SYSTEM_ID>" +
                            "<GROUP_SYSTEM_NAME>Default Groupsystem Contorion</GROUP_SYSTEM_NAME>" +
                            '<CATALOG_STRUCTURE type="root">' +
                            "<GROUP_ID>1</GROUP_ID>" +
                            "<GROUP_NAME>Katalog</GROUP_NAME>" +
                            "<PARENT_ID>0</PARENT_ID>" +
                            "<GROUP_ORDER>1</GROUP_ORDER>" +
                            "</CATALOG_STRUCTURE>" +
                            '<CATALOG_STRUCTURE type="leaf">' +
                            "<GROUP_ID>2</GROUP_ID>" +
                            "<GROUP_NAME>Produkte</GROUP_NAME>" +
                            "<PARENT_ID>1</PARENT_ID>" +
                            "<GROUP_ORDER>2</GROUP_ORDER>" +
                            "</CATALOG_STRUCTURE>" +
                            "</CATALOG_GROUP_SYSTEM>")



    def __extractInitials(self, usplit):
        initials = ""
        for elem in usplit:
            if len(elem) > 0:
                initials += elem[0].upper()
        
        return initials

    def __determineInitials(self):
        userName = getpass.getuser()
        if userName is None:
            return "BC_TEMP"
        
        logging.debug("Username: {0}".format(userName))
        usplit = []
        if len(userName.split(" ")) > 1:
            usplit = userName.split(" ")
        if len(userName.split(".")) > 1:
            usplit = userName.split(".")

        if len(usplit) > 1 and len(usplit[0].split("-")) > 1:
            usplit = usplit[0].split("-").append(usplit[1])
        initials = self.__extractInitials(usplit)
            
        return initials

    def __createGenerationDate(self): 
        now = datetime.now()
        generationDate = now.strftime("%Y-%m-%d")
        generationTime = now.strftime("%H:%M:%S")
        dateTime = Element("DATETIME", { "type" : "generation_date" })
        SubElement(dateTime, "DATE").text = generationDate
        SubElement(dateTime, "TIME").text = generationTime
        return dateTime

    def __createCatalogInfo(self):
        initials = self.__determineInitials()
        logging.debug("Initialen: {0}".format(initials))

        dateKz = datetime.now().strftime("%Y%m%d")
        catalog = Element("CATALOG")
        SubElement(catalog, "LANGUAGE").text = "deu"
        SubElement(catalog, "CATALOG_ID").text = dateKz + "_" + initials
        SubElement(catalog, "CATALOG_VERSION").text = "1.0"
        SubElement(catalog, "CATALOG_NAME").text = dateKz + "-" + self._merchant.title() + "-Update_" + initials
        catalog.append(self.__createGenerationDate())
        SubElement(catalog, "CURRENCY").text = "EUR"
        return catalog

    def __createSubElementWithNameContorion(self, tag):
        element = Element(tag)
        SubElement(element, tag + "_NAME").text = "Contorion GmbH"
        return element
    
    def __createHeaderElement(self):
        ''' Create Header of BMEcat
        '''
        header = Element("HEADER")
        SubElement(header, "GENERATOR_INFO").text = "BMEcatConverter Contorion"
        header.append(self.__createCatalogInfo())
        header.append(self.__createSubElementWithNameContorion("BUYER"))
        header.append(self.__createSubElementWithNameContorion("SUPPLIER"))
        
        return header

    def __prettyFormattedOutput(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        return etree.tostring(elem, encoding="UTF-8", pretty_print=True, xml_declaration=True)
    
    def __createArticleCatalogMapping(self):
        mapping = []
        for articleType, articles in self._articles.items():
            for article in articles:
                parent = Element("ARTICLE_TO_CATALOGGROUP_MAP")
                SubElement(parent,"ART_ID").text = article.productId
                SubElement(parent,"CATALOG_GROUP_ID").text = "2"
                SubElement(parent,"ARTICLE_TO_CATALOGGROUP_MAP_ORDER").text = "2"
                mapping.append(parent)
        return mapping