'''
Created on 17.05.2017

@author: henrik.pilz
'''
from . import ValidatingXmlObject


class Variant(ValidatingXmlObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.value = None
        self.productIdSuffix = None

    def __eq__(self, other):
        return self.value == other.value and self.productIdSuffix == other.productIdSuffix
    
    def __ne__(self, other):
        return not self.__eq__(other)
           
    def validate(self, raiseException=False):
        errMsg = None
        if self.value is None:
            errMsg = "Die Variante wurde nicht definiert."
            super().logError(errMsg, raiseException)
        if self.productIdSuffix is None:
            errMsg= "Das Suffix fuer die Variante " + str(self.value) + " wurde nicht definiert."
            super().logError(errMsg, raiseException)
