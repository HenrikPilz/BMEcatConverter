'''
Created on 17.05.2017

@author: henrik.pilz
'''
from datamodel.comparableEqual import ComparableEqual
from datamodel.xmlObject import ValidatingXMLObject


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
        super().valueNotNone(self.value, "Die Variante wurde nicht definiert.", raiseException)
        super().valueNotNone(self.productIdSuffix, "Das Suffix fuer die Variante '{0}' wurde nicht definiert.".format(str(self.value)), raiseException)

    def toXml(self, raiseExceptionOnValidate=True):
        xmlVariant = super().validateAndCreateBaseElement("VARIANT", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(xmlVariant, "FVALUE", self.value)
        super().addMandatorySubElement(xmlVariant, "SUPPLIER_AID_SUPPLEMENT", self.productIdSuffix)
        return xmlVariant
