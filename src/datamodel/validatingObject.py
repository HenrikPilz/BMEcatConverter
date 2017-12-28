'''
Created on 07.10.2017

@author: Henrik Pilz
'''
from abc import abstractmethod
from array import array
import logging

from lxml.etree import SubElement, Element


class NoValueGivenException(Exception):
    '''
    Exception thrown when no Value is given.
    '''


class FormulaFoundException(Exception):
    '''
    Exception thrown if an excel formula entry is found.
    '''


class ComparableEqual(object):
    '''
    Interface Class for a Class which are comparable
    '''

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def checkListForEquality(self, lhs, rhs):
        for leftItem in lhs:
            if leftItem not in rhs:
                return False

        for rightItem in rhs:
            if rightItem not in lhs:
                return False
        return True


class ValidatingObject(object):
    '''
    Interface Class for a Class which validates its content
    '''

    def add(self, attributeName, attributeValue):
        if attributeValue is None:
            return
        try:
            if not isinstance(getattr(self, attributeName), (list, array)):
                setattr(self, attributeName, attributeValue)
            else:
                attributeList = getattr(self, attributeName)
                if isinstance(attributeValue, ValidatingObject):
                    errorMessage = "Item '{0}' could not be added to List '{1}'.".format(attributeValue, attributeName)
                    self.addToListIfValid(attributeValue, attributeList, errorMessage)
                else:
                    if attributeValue not in attributeList:
                        attributeList.append(attributeValue)
        except AttributeError as ae:
            logging.error("Klassenattribut nicht gefunden: {0}".format(str(ae)))

    def validateList(self, listToValidate, additionalMessage, raiseException):
        try:
            for listItem in listToValidate:
                listItem.validate(raiseException)
        except Exception as e:
            raise Exception(additionalMessage + " :: " + str(e))

    @abstractmethod
    def validate(self, raiseException=False):
        raise NotImplementedError("Please implement 'validate' in your class '{0}".format(__file__))

    def validateIfNotNoneOrEmpty(self, elementToCheck, noneOrEmptyMessage, validationMessage, raiseException=False):
        '''
        if the attribute is a list and the list is not None or Empty
        every listitem is validated.
        '''
        self.validateIfNotNoneOrEmptyRaiseException(elementToCheck, noneOrEmptyMessage, validationMessage, raiseException, False)

    def validateIfNotNoneOrEmptyRaiseException(self, elementToCheck, noneOrEmptyMessage, validationMessage,
                                               raiseException=False, raiseExceptionIfNoneOrEmpty=True):
        '''
        if the attribute is a list and the list is not None or Empty
        every listitem is validated.
        Raises an Exception if the list is None or Empty
        '''
        if self.valueNotNoneOrEmpty(elementToCheck, noneOrEmptyMessage, raiseExceptionIfNoneOrEmpty):
            self.validateList(elementToCheck, validationMessage, raiseException)

    def valueNotNone(self, attribute, message=None, raiseException=False):
        if attribute is None:
            self.logError(message, raiseException)
            return False
        return True

    def valueNotNoneOrEmpty(self, attribute, message=None, raiseException=False):
        if not self.valueNotNone(attribute, message, raiseException):
            return False
        isNotEmpty = True
        if isinstance(attribute, str):
            isNotEmpty = len(attribute.strip()) > 0
        elif isinstance(attribute, (list, array)):
            isNotEmpty = len(attribute) > 0
        else:
            isNotEmpty = len(str(attribute).strip()) > 0
        if isNotEmpty:
            return True
        self.logError(message, raiseException)
        return False

    def logError(self, errMsg=None, raiseException=False):
        '''
         Taking an ErrorMessage, logging it and if wanted throwing an Exception
        '''
        if errMsg is not None:
            logging.error(errMsg)
        if raiseException:
            raise Exception(errMsg)

    def addToListIfValid(self, item, listToAddTo, errorMessage, raiseException=True):
        if item is None:
            return False
        try:
            self.__determineOrderIfNeeded(item, listToAddTo)
            item.validate(raiseException)
            if item not in listToAddTo:
                listToAddTo.append(item)
                return True
        except Exception as ve:
            logging.warning(errorMessage + "{0}".format(str(ve)))
        return False

    def __determineOrderIfNeeded(self, item, orderedList):
        try:
            if getattr(item, "order") is None or int(item.order) <= 0:
                self.__determineOrder(item, orderedList)
        except AttributeError:
            pass

    def __determineOrder(self, item, orderedList):
        maxItem = max(orderedList, key=lambda item: int(item.order), default=None)
        if maxItem is None:
            item.order = 1
        else:
            item.order = int(maxItem.order) + 1

    def valueNotEmptyOrNoneAndNotIn(self, value, errorMessageNone, listToCheck, errorMessageNotIn, raiseException=False):
        if self.valueNotNoneOrEmpty(value, errorMessageNone, raiseException) and value not in listToCheck:
            self.logError("{0} Wert: {1}".format(errorMessageNotIn, str(value)), raiseException)

    def checkAttributesForFormulas(self, listOfAttributeNames):
        for attributeName in listOfAttributeNames:
            value = self.__getattribute__(attributeName)
            if isinstance(value, (array, list)):
                for entry in value:
                    self.__checkValueForFormulaEntry(entry, attributeName)
            else:
                self.__checkValueForFormulaEntry(value, attributeName)

    def __checkValueForFormulaEntry(self, value, attributeName):
        if str(value).startswith("="):
            raise FormulaFoundException("Im Objekt vom Typ '{0}' wurde im Feld {1} ein Formeleintrag gefunden.".format(self.__class__.__name__, attributeName))


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
