'''
Created on 07.10.2017

@author: Henrik Pilz
'''
from abc import abstractmethod
import logging


class ValidatingXmlObject(object):
    '''
    Interface Class for a Class which validates its content
    '''
    
    def __init__(self):
        super().__init__()

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
    
    @abstractmethod
    def validate(self, raiseException=False):
        raise NotImplementedError("Please implement 'validate' in your class '{0}".format(__file__))
    
    def logError(self, errMsg, raiseException=False):
        '''
         Taking an ErrorMessage, logging it and if wanted throwing an Exception
        '''
        logging.error(errMsg)
        if raiseException:
            raise Exception(errMsg)

    @abstractmethod
    def toXml(self):
        raise NotImplementedError("Please implement 'toXml' in your class '{0}".format(__file__))