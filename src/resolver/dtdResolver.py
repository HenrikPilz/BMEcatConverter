'''
Created on 30.06.2017

@author: henrik.pilz
'''
from xml.sax.handler import EntityResolver
import logging
import os


class DTDResolver(EntityResolver):
    '''
    classdocs
    '''

    def __init__(self, params=None):
        '''
        Constructor
        '''
        self.bmecatVersions = {}
        bmecatDataPath = os.path.join(os.path.dirname(__file__), "..", "..", "documents", "BMEcat", "version")

        self._checkSubDirectories(bmecatDataPath)

    def _checkSubDirectories(self, path):
        if os.path.isfile(path) and path.endswith('.dtd'):
            self.bmecatVersions[os.path.basename(path)] = os.path.abspath(path)
        if os.path.isdir(path):
            for subelement in os.listdir(path):
                self._checkSubDirectories(os.path.join(path, subelement))

    def resolveEntity(self, publicId, systemId):
        """Resolve the system identifier of an entity and return either
        the system identifier to read from as a string, or an InputSource
        to read from."""
        logging.debug("ResolverEntity: PID: '{0}' /SID: '{1}'".format(publicId, systemId))
        if systemId in self.bmecatVersions.keys():
            return self.bmecatVersions[systemId]
        else:
            return systemId
