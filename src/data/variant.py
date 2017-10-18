'''
Created on 17.05.2017

@author: henrik.pilz
'''
from . import ValidatingObject, XmlObject, ComparableEqual
from lxml.etree import Element

class Variant(ValidatingObject, XmlObject, ComparableEqual):
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
            return self.value == other.value and self.productIdSuffix == other.productIdSuffix
               
    def validate(self, raiseException=False):
        errMsg = None
        if self.value is None:
            errMsg = "Die Variante wurde nicht definiert."
            super().logError(errMsg, raiseException)
        if self.productIdSuffix is None:
            errMsg= "Das Suffix fuer die Variante " + str(self.value) + " wurde nicht definiert."
            super().logError(errMsg, raiseException)

    def toXml(self):
        self.validate(True)
        xmlVariant = Element("VARIANT")
        super().addMandatorySubElement(xmlVariant, "FVALUE", self.value)
        super().addMandatorySubElement(xmlVariant, "SUPPLIER_AID_SUPPLEMENT", self.productIdSuffix)
        return xmlVariant