'''
Created on 30.06.2017

@author: henrik.pilz
'''
import logging
import os
from xml.sax.handler import EntityResolver


class DTDResolver( EntityResolver ):
    '''
    classdocs
    '''


    def __init__( self, params = None ):
        '''
        Constructor
        '''
        self.bmecatVersions = {}
        self.bmecatDataPath = os.path.join( os.path.dirname( __file__ ), "..", "..", "documents", "BMEcat", "version" )

        for dirname in os.listdir( self.bmecatDataPath ):
            currentPath = os.path.join( self.bmecatDataPath, dirname )
            if os.path.isdir( currentPath ):
                for filename in os.listdir( currentPath ):
                    filePath = os.path.join( currentPath, filename )
                    if os.path.isfile( filePath ):
                        self.bmecatVersions[filename] = os.path.abspath( filePath )

    def resolveEntity( self, publicId, systemId ):
        """Resolve the system identifier of an entity and return either
        the system identifier to read from as a string, or an InputSource
        to read from."""
        logging.debug( "ResolverEntity: PID: '{0}' /SID: '{1}'".format( publicId, systemId ) )
        if systemId in self.bmecatVersions.keys():
            return  self.bmecatVersions[systemId]
        else:
            return systemId
