'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject


class TreatmentClass(ValidatingXmlObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.classType = None
        self.value = None

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            return self.classType == other.classType and self.value == other.value
        
    def validate(self, raiseException=False):
        if self.classType is None:
            super().logError("Es muss eine Klassifizierung angegeben werden.", raiseException)
        if self.value is None:
            logging.info("Es wurde kein Wert zur Klassifizierung angegeben.")