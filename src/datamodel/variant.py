'''
Created on 17.05.2017

@author: henrik.pilz
'''
from . import ValidatingXMLObject, ComparableEqual
from lxml.etree import Element

class Variant(ValidatingXMLObject, ComparableEqual):
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
        if not super().__eq__(other):
            return False
        else:
            return str(self.value) == str(other.value) and str(self.productIdSuffix) == str(other.productIdSuffix)
               
    def validate(self, raiseException=False):
        errMsg = None
        if self.value is None:
            errMsg = "Die Variante wurde nicht definiert."
            super().logError(errMsg, raiseException)
        if self.productIdSuffix is None:
            errMsg= "Das Suffix fuer die Variante " + str(self.value) + " wurde nicht definiert."
            super().logError(errMsg, raiseException)

    def toXml(self):
        xmlVariant = super().validateAndCreateBaseElement("VARIANT")
        super().addMandatorySubElement(xmlVariant, "FVALUE", self.value)
        super().addMandatorySubElement(xmlVariant, "SUPPLIER_AID_SUPPLEMENT", self.productIdSuffix)
        return xmlVariant