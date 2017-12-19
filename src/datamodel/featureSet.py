'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
import os

from datamodel.validatingObject import ComparableEqual
from datamodel.validatingObject import ValidatingXMLObject
from mapping.blacklist import Blacklist


class FeatureSet(ValidatingXMLObject, ComparableEqual):

    __baseDirectory = os.path.join(os.path.dirname(__file__), "..", "..", "documents", "BMEcat", "version")
    __featureBlacklist = Blacklist(os.path.join(__baseDirectory, "FeatureBlacklist.csv"))

    def __init__(self):
        self.referenceSystem = None
        self.referenceGroupName = None
        self.referenceGroupId = None
        self.features = []

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            return super().checkListForEquality(self.features, other.features)

    def addFeature(self, feature):
        if self.__featureBlacklist.contains(feature.name):
            logging.info("Attribut wird nicht gespeichert, da es auf der Blacklist ist.")
        else:
            self.addToListIfValid(feature, self.features, "Das Attribut enthaelt keine validen Werte. Es wird nicht hinzugefuegt. ")

    def validate(self, raiseException=False):
        if self.referenceGroupName is not None and self.referenceGroupId is not None:
            super().logError("Es darf nur entweder eine Referenzgruppen ID oder ein Referenzgruppenname angegeben werden.", raiseException)
        if super().valueNotNoneOrEmpty(self.features, "Keine Attribute fuer diese Attributgruppe vorhanden!", raiseException):
            for feature in self.features:
                feature.validate(raiseException)

    def __len__(self):
        return len(self.features)

    def toXml(self, raiseExceptionOnValidate=True):
        xmlFeatureSet = super().validateAndCreateBaseElement("ARTICLE_FEATURES", raiseExceptionOnValidate=raiseExceptionOnValidate)
        super().addOptionalSubElement(xmlFeatureSet, "REFERENCE_FEATURE_SYSTEM_NAME", self.referenceSystem)
        super().addOptionalSubElement(xmlFeatureSet, "REFERENCE_FEATURE_GROUP_ID", self.referenceGroupId)
        super().addOptionalSubElement(xmlFeatureSet, "REFERENCE_FEATURE_GROUP_NAME", self.referenceGroupName)
        super().addListOfSubElements(xmlFeatureSet, sorted(self.features, key=lambda feature: feature.order), raiseExceptionOnValidate)
        return xmlFeatureSet
