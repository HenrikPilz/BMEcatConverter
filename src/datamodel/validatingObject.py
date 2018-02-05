'''
Created on 07.10.2017

@author: Henrik Pilz
'''
from abc import abstractmethod
from array import array
import logging


class FormulaFoundException(Exception):
    '''
    Exception thrown if an excel formula entry is found.
    '''


class ValidatingObject(object):
    '''
    Interface Class for a Class which validates its content
    '''

    def add(self, attributeName, attributeValue):
        '''
        Validating, if the given Value is empty and if not adds it to the attribute given by the attrirbuteName.
        @param attributeName: Name of the attribute to add the value to. Can be of any basic type (int, str, float, ...)
                              or array or list.
        @param attributeValue: the value which should be added.
        @return: None
        @raise Exception: if the Attribute is not found
        '''
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
            self.logError("Klassenattribut nicht gefunden: {0}".format(str(ae)), True)

    @classmethod
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
            if raiseException:
                logging.error(errMsg)
            else:
                logging.warning(errMsg)
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
        except FormulaFoundException as ffe:
            raise ffe
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

    def _trimIfString(self, value):
        if isinstance(value, str):
            return value.strip(" \n\r\t")
        else:
            return value
