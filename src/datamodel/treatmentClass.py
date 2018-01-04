'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging

from datamodel.validatingObject import ComparableEqual
from datamodel.validatingObject import ValidatingXMLObject


class TreatmentClass(ValidatingXMLObject, ComparableEqual):
    '''
    classdocs
    '''

    def __init__(self, classType=None):
        '''
        Constructor
        '''
        self.classType = classType
        self.value = None

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            return self.classType == other.classType and self.value == other.value

    def validate(self, raiseException=False):
        super().valueNotNone(self.classType, "Es muss eine Klassifizierung angegeben werden.", raiseException)
        super().valueNotNone(self.value, "Es wurde kein Wert zur Klassifizierung angegeben.", False)

    def toXml(self, raiseExceptionOnValidate=True):
        xmlElement = super().validateAndCreateBaseElement("SPECIAL_TREATMENT_CLASS", { "type" : self.classType }, raiseExceptionOnValidate)
        xmlElement.text = self.value
        return xmlElement
