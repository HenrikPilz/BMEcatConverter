'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging
from . import ValidatingXmlObject
from lxml.etree import Element


class FeatureSet(ValidatingXmlObject):
    def __init__(self):
        self.referenceSytem = None
        self.referenceGroupName = None
        self.referenceGroupId = None
        self.features = []
        
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:
            featuresEqual = super().checkListForEquality(self.features, other.features)
            return featuresEqual and self.referenceGroupId == other.referenceGroupId and self.referenceSytem == other.referenceSytem

    def addFeature(self,feature):
        try:
            feature.validate(True)
            self.features.append(feature)
        except Exception as ve:
            logging.info("Das Attribut enthaelt keine validen Werte. Es wird nicht hinzugefuegt. {0}".format(str(ve)))
        
    def validate(self, raiseException=False):
        if self.referenceGroupName is not None and self.referenceGroupId is not None:
            super().logError("Es darf nur entweder eine Referenzgruppen ID oder ein Referenzgruppenname angegeben werden.", raiseException)
        if self.features is None or len(self.features) == 0:
            logging.warning("Keine Attribute fuer diese Attributgruppe vorhanden!")
        else:
            for feature in self.features:
                feature.validate(raiseException)

    def __len__(self):
        return len(self.features)
    
    def toXml(self):
        self.validate(True)
        xmlFeatureSet = Element("ARTICLE_FEATURES")
        super().addOptionalSubElement(xmlFeatureSet, "REFERENCE_FEATURE_SYSTEM_NAME", self.referenceSytem)
        super().addOptionalSubElement(xmlFeatureSet, "REFERENCE_FEATURE_GROUP_ID", self.referenceGroupId)
        super().addOptionalSubElement(xmlFeatureSet, "REFERENCE_FEATURE_GROUP_NAME", self.referenceGroupName)
        for feature in self.features:
            xmlFeatureSet.append(feature.toXml())
