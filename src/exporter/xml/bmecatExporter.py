'''
Created on 12.05.2017

@author: henrik.pilz
'''
from datetime import datetime
import getpass
import logging

from lxml import etree
from lxml.etree import Element
from lxml.etree import SubElement
from error import DataErrorException


class BMEcatExporter(object):

    __strict_validation = 'strict'

    def __init__(self, articles, filename, validation=__strict_validation):
        self._articles = articles  # dict!
        self._filename = filename
        self._validation = validation

    def __createArticleElements(self):
        articleElements = []
        for articleType, articles in self._articles.items():
            articleElements.extend(self.__createArticleElementsForSet(articles, articleType))
        return articleElements

    def __createArticleElementsForSet(self, articles, articleType='new'):
        articleElements = []
        exceptions = []
        for article in articles:
            try:
                articleElement = article.toXml(articleType, self._validation.lower() == BMEcatExporter.__strict_validation)
                articleElements.append(articleElement)
            except Exception as e:
                exceptions.append(e)
        if len(exceptions) > 0:
            for entry in exceptions:
                logging.error(str(entry))
            raise DataErrorException("BMEcat not complete. Found {0} errors.".format(len(exceptions)))
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
                         '<BMECAT version="1.2" xml:lang="de" ' +
                         'xmlns="http://www.bmecat.org/bmecat/1.2/bmecat_new_catalog" />')

    def __createCatalogGroupSystemElement(self):
        return etree.XML("<CATALOG_GROUP_SYSTEM>" +
                         "<GROUP_SYSTEM_ID>1</GROUP_SYSTEM_ID>" +
                         "<GROUP_SYSTEM_NAME>Default Groupsystem</GROUP_SYSTEM_NAME>" +
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
            secondPart = usplit[1:]
            usplit = usplit[0].split("-")
            usplit.extend(secondPart)

        return self.__extractInitials(usplit)

    def __createGenerationDate(self):
        now = datetime.now()
        generationDate = now.strftime("%Y-%m-%d")
        generationTime = now.strftime("%H:%M:%S")
        dateTime = Element("DATETIME", { "type" : "generation_date" })
        SubElement(dateTime, "DATE").text = generationDate
        SubElement(dateTime, "TIME").text = generationTime
        return dateTime

    def __createCatalogInfo(self):
        initials = "NotSet"
        try:
            initials = self.__determineInitials()
        except Exception:
            logging.warning("Initialen konnten nicht ermittelt werden.")

        logging.debug("Initialen: {0}".format(initials))

        dateYMD = datetime.now().strftime("%Y%m%d")
        catalogId = datetime.now().strftime("%Y%m%d%H%M%S")

        catalog = Element("CATALOG")
        SubElement(catalog, "LANGUAGE").text = "deu"
        SubElement(catalog, "CATALOG_ID").text = catalogId + "_" + initials
        SubElement(catalog, "CATALOG_VERSION").text = "1.0"
        SubElement(catalog, "CATALOG_NAME").text = dateYMD + "-" + self._validation.title() + "-Update_" + initials
        catalog.append(self.__createGenerationDate())
        SubElement(catalog, "CURRENCY").text = "EUR"
        return catalog

    def __createSubElement(self, tag):
        element = Element(tag)
        SubElement(element, tag + "_NAME").text = tag
        return element

    def __createHeaderElement(self):
        ''' Create Header of BMEcat
        '''
        header = Element("HEADER")
        SubElement(header, "GENERATOR_INFO").text = "BMEcatConverter"
        header.append(self.__createCatalogInfo())
        header.append(self.__createSubElement("BUYER"))
        header.append(self.__createSubElement("SUPPLIER"))

        return header

    def __prettyFormattedOutput(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        return etree.tostring(elem, encoding="UTF-8", pretty_print=True, xml_declaration=True)

    def __createArticleCatalogMapping(self):
        mapping = []
        for _, articles in self._articles.items():
            for article in articles:
                parent = Element("ARTICLE_TO_CATALOGGROUP_MAP")
                SubElement(parent, "ART_ID").text = str(article.productId)
                SubElement(parent, "CATALOG_GROUP_ID").text = "2"
                SubElement(parent, "ARTICLE_TO_CATALOGGROUP_MAP_ORDER").text = "2"
                mapping.append(parent)
        return mapping
