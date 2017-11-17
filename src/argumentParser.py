'''
Created on 01.09.2017

@author: henrik.pilz
'''

import getopt
import logging


class HelpCalledException( Exception ):
    '''
    Exception if Help is called
    '''


class MissingArgumentException( Exception ):
    '''
    Exception if an argument is Missing
    '''


class ArgumentParser():
    '''
    classdocs
    '''
    def __init__( self ):
        self.inputfile = None
        self.outputfile = None
        self.merchant = 'fiege'
        self.manufacturer = None
        self.dateformat = None
        self.separatorMode = None

    def parse( self, argv ):
        opts, _ = getopt.getopt( 
                                argv,
                                "hi:o:",
                                ["merchant=",
                                 "manufacturer=",
                                 "dateformat=",
                                 "separators="]
                                   )
        logging.debug( "Options: ", opts )

        for opt, arg in opts:
            logging.debug( "Option: " + opt )
            logging.debug( "Argument: " + arg )
            self._checkAndDetermineArgument( opt, arg )

        self._validateArguments()
        self.logData()

    def _checkAndDetermineArgument( self, opt, arg ):
        if opt == '-h':
            raise HelpCalledException()
        if opt == "-i":
            self.inputfile = arg
        if opt == "-o":
            self.outputfile = arg
        if opt == "--manufacturer":
            self.manufacturer = arg
        if opt == "--merchant":
            self.merchant = arg
        if opt == "--separators":
            self.separatorMode = arg
        if opt == "--dateformat":
            self.dateformat = arg

    def _validateArguments( self ):
        if self.inputfile is None:
            raise MissingArgumentException( "Inputfile is missing." )
        if self.outputfile is None:
            raise MissingArgumentException( "Outputfile is missing." )
        if self.dateformat is None:
            raise MissingArgumentException( "Dateformat  is missing." )
        if self.separatorMode is None:
            raise MissingArgumentException( "SeparateorMode  is missing." )

    def logData( self ):
        logging.info( "Input file is {0}".format( self.inputfile ) )
        logging.info( "Output file is {0}".format( self.outputfile ) )
        if self.merchant is not None:
            logging.info( "Merchant: {0}".format( self.merchant ) )
        if self.manufacturer is not None:
            logging.info( "Manufacturer: {0}".format( self.manufacturer ) )
