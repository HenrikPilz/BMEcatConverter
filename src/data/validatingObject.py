'''
Created on 07.10.2017

@author: Henrik Pilz
'''
from abc import abstractmethod
from lxml.etree import SubElement
import logging

class NoValueGivenException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ValidatingObject(object):
    '''
    Interface Class for a Class which validates its content
    '''
    
    def __init__(self):
        super().__init__()
    
    def valueNotNoneOrEmpty(self, attribute, message, raiseException=False):
        isEmpty = False
        if type(attribute) == 'str':
            isEmpty = len(attribute.strip())== 0
        else:
            isEmpty = len(attribute) == 0
        
        if attribute is None or isEmpty:
            self.logError(message, raiseException)
            return False
        return True

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)


    def valueNotNone(self, attribute, message, raiseException=False):
        if attribute is None:
            self.logError(message, raiseException)
            return False
        return True
    
    def logError(self, errMsg, raiseException=False):
        '''
         Taking an ErrorMessage, logging it and if wanted throwing an Exception
        '''
        logging.error(errMsg)
        if raiseException:
            raise Exception(errMsg)



class ValidatingXmlObject(ValidatingObject):
    '''
    Interface Class for a Class which validates its content
    '''
    
    def __init__(self):
        super().__init__()

    @classmethod
    def checkListForEquality(self, lhs, rhs):
        for leftItem in lhs:
            if leftItem not in rhs:
                return False

        for rightItem in rhs:
            if rightItem not in lhs:
                return False
        return True
    
    @abstractmethod
    def validate(self, raiseException=False):
        raise NotImplementedError("Please implement 'validate' in your class '{0}".format(__file__))
    
    @abstractmethod
    def toXml(self):
        raise NotImplementedError("Please implement 'toXml' in your class '{0}".format(__file__))

    def addMandatorySubElement(self, parent, tag, value):
        if value is None:
            raise NoValueGivenException("Kein Wert übergeben.")
        SubElement(parent, tag).text = value
    
    def addOptionalSubElement(self, parent, tag, value):
        if value is not None:
            SubElement(parent, tag).text = value

