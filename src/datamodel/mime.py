'''
Created on 05.05.2017

@author: henrik.pilz
'''
from datamodel.validatingObject import ComparableEqual
from datamodel.validatingObject import ValidatingXMLObject


class Mime(ValidatingXMLObject, ComparableEqual):

    __allowedTypes = [ "url",
                       "application/pdf",
                       "image/jpg",
                       "image/jpeg",
                       "image/tif",
                       "image/tiff",
                       "text/html",
                       "text/plain",
                       "image/eps",
                       "image/png",
                       "image/gif"
                       ]
    __allowedPurposes = [ "thumbnail", "normal", "detail", "data_sheet", "logo", "others" ]
    __allowedCombinations = {}

    def __init__(self):
        self.source = None
        self.mimeType = None
        self.description = None
        self.altenativeContent = None
        self.purpose = None
        self.order = None

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            return self.source == other.source and self.mimeType == other.mimeType

    def validate(self, raiseException=False):
        super().valueNotNone(self.source, "Kein Bildpfad angegeben.", raiseException)
        self.__convertPathToLowerCase()
        super().valueNotNone(self.order, "Bildreihenfolge fehlerhaft: " + str(self.order), raiseException)
        super().valueNotEmptyOrNoneAndNotIn(self.mimeType, "Bildtyp nicht gesetzt.", self.__allowedTypes, "Bildtyp fehlerhaft.", raiseException)
        super().valueNotEmptyOrNoneAndNotIn(self.purpose, "Bildverwendung nicht gesetzt.", self.__allowedPurposes, "Bildverwendung fehlerhaft.", raiseException)
        self.checkAttributesForFormulas(['source', 'order', 'mimeType', 'purpose', 'description'])

    def toXml(self, raiseExceptionOnValidate=True):
        mimeElement = super().validateAndCreateBaseElement("MIME", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addMandatorySubElement(mimeElement, "MIME_SOURCE", self.source)
        super().addMandatorySubElement(mimeElement, "MIME_TYPE", self.mimeType)
        super().addMandatorySubElement(mimeElement, "MIME_PURPOSE", self.purpose)
        super().addMandatorySubElement(mimeElement, "MIME_ORDER", self.order)
        super().addOptionalSubElement(mimeElement, "MIME_DESCR", self.description)
        super().addOptionalSubElement(mimeElement, "MIME_ALT", self.altenativeContent)
        return mimeElement

    def __convertPathToLowerCase(self):
        '''
        Entfernt '/' und Leerzeichen im Pfad, aber NICHT im Dateinamen.
        Erzwingt eine Kleinschreibung aller Pfadbestandteile, bis auf den Dateinamen.
        Im Dateinamen werden die Leerzeichen durch Unterstriche ersetzt.
        '''
        if self.source.find("/") >= 0:
            filepath = self.source.strip(" /").split("/")
            self.source = "/".join([elem.replace(" ", "").lower() for elem in filepath[:-1]]) + "/" + filepath[-1].replace(" ", "_")
