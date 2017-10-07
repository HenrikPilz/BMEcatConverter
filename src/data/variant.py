'''
Created on 17.05.2017

@author: henrik.pilz
'''
from . import ValidatingObject


class Variant(ValidatingObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.value = None
        self.productIdSuffix = None
       
    def validate(self, raiseException=False):
        errMsg = None
        if self.value is None:
            errMsg = "Die Variante wurde nicht definiert."
            super().logError(errMsg, raiseException)
        if self.productIdSuffix is None:
            errMsg= "Das Suffix fuer die Variante " + str(self.value) + " wurde nicht definiert."
            super().logError(errMsg, raiseException)
