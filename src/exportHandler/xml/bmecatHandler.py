'''
Created on 12.05.2017

@author: henrik.pilz
'''
from datetime import datetime
import os

from lxml import etree
from lxml.etree import Element

class BMEcatHandler(object):
    
    def __createArticleElements(self, articles):
        articleElements = []
        for articleType in articles.keys():
            articleElements.extend(self.__createArticleElementsForSet(articles[articleType]))
        return articleElements

    def __createArticleElementsForSet(self, articles):
        articleElements = []
        for article in articles:
            articleElements.append(article.toXmlElemnt())
        return articleElements
    
    def writeBMEcatAsXML(self, filename, articles):
        with open(filename, "wb") as file:
            bmecat = self.__createBMEcatRootElement()
            bmecat.append(self.__createHeaderElement())
            
            newCatalog = Element("T_NEW_CATALOG")
            newCatalog.append(self.__createCatalogGroupSystemElement())
            bmecat.append(newCatalog)    
            newCatalog.extend(self.__createArticleElements(articles))
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

    def __createHeaderElement(self):
        ''' Create Header of BMEcat
        '''
        userName = os.environ["USERNAME"]
        usplit = userName.split(" ")
        initals = usplit[0][0] + usplit[1][0]
        
        now = datetime.now()

        generationDate = now.strftime("%Y-%m-%d")
        dateKz = now.strftime("%Y%m%d")
        generationTIme = now.strftime("%H:%M:%S")
        return etree.XML("<HEADER>" +
                            "<GENERATOR_INFO>BMEcatConverter Contorion</GENERATOR_INFO>" +
                            "<CATALOG>" +
                            "<LANGUAGE>deu</LANGUAGE>" +
                            "<CATALOG_ID>" + dateKz + "_" + initals +"</CATALOG_ID>" +
                            "<CATALOG_VERSION>1.0</CATALOG_VERSION>" +
                            "<CATALOG_NAME>" + dateKz + "-Fiege-Update_" + initals +"</CATALOG_NAME>" +
                            '<DATETIME type="generation_date">' +
                            "<DATE>" + generationDate + "</DATE>" +
                            "<TIME>"+ generationTIme + "</TIME>" +
                            "</DATETIME>" +
                            "<CURRENCY>EUR</CURRENCY>" +
                            "</CATALOG>" +
                            "<BUYER>" +
                            "<BUYER_NAME>Contorion GmbH</BUYER_NAME>" +
                            "</BUYER>" +
                            "<SUPPLIER>" +
                            "<SUPPLIER_NAME>Contorion GmbH</SUPPLIER_NAME>" +
                            "</SUPPLIER>" +
                            "</HEADER>")

    def __prettyFormattedOutput(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        return etree.tostring(elem, encoding="UTF-8", pretty_print=True, xml_declaration=True)
    