'''
Created on 07.10.2017

@author: Henrik Pilz
'''
from abc import abstractmethod

from lxml.etree import SubElement, Element

from datamodel.validatingObject import ValidatingObject


class NoValueGivenException(Exception):
    '''
    Exception thrown when no Value is given.
    '''


class XMLObject(object):
    '''
    Interface Class for a Class which writes its content to XML
    '''

    @abstractmethod
    def toXml(self):
        raise NotImplementedError("Please implement 'toXml' in your class '{0}".format(__file__))

    def addMandatorySubElement(self, parent, tag, value):
        '''
        Erstellt eiin Child-Element und wirft eine Exception, falls value nicht None
        '''
        if value is None:
            raise NoValueGivenException("'{0}' Kein Wert übergeben.".format(tag))
        subElement = SubElement(parent, tag)
        subElement.text = str(value).strip()
        return subElement

    def addOptionalSubElement(self, parent, tag, value):
        '''
        Erstellt eiin Child-Element, falls value nicht None
        '''
        if value is not None and len(str(value)) > 0:
            return self.addMandatorySubElement(parent, tag, value)
        return None

    def addListOfSubElements(self, parent, listOfSubElements, raiseExceptionOnValidate=True):
        for element in listOfSubElements:
            parent.append(element.toXml(raiseExceptionOnValidate=raiseExceptionOnValidate))

    def addDateTimeSubElement(self, parent, dateType, date):
        dateTimeSubElement = SubElement(parent, "DATETIME", { "type"  : dateType})
        dateSubElement = SubElement(dateTimeSubElement, "DATE")
        dateSubElement.text = date.strftime("%Y-%m-%d")
        timeSubElement = SubElement(dateTimeSubElement, "TIME")
        timeSubElement.text = date.strftime("%H:%M:%S")


class ValidatingXMLObject(ValidatingObject, XMLObject):
    '''
    Interface Class for a Class which validates its content and writes its Content to XML
    '''

    def validateAndCreateBaseElement(self, tagname, attributes=None, raiseExceptionOnValidate=True):
        self.validate(raiseExceptionOnValidate)
        return Element(tagname, attributes)
