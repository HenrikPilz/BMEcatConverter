'''
Created on 01.09.2017

@author: henrik.pilz
'''

import getopt
import logging

class HelpCalledException(Exception):
    '''
    Exception if Help is called
    '''

class MissingArgumentException(Exception):
    '''
    Exception if an argument is Missing
    '''

class ArgumentParser():
    '''
    classdocs
    '''
    def __init__(self):
        self._inputfile = None
        self._outputfile = None
        self._merchant = 'fiege'
        self._manufacturer = None
        self._dateformat = None
        self._separatorMode = None
        
    def parse(self, argv):
        opts, args = getopt.getopt(argv,"hi:o:", ["merchant=", "manufacturer=", "dateformat=", "separators="])
        print("Options: ", opts)
    
        for opt, arg in opts:
            logging.debug("Option: " + opt)
            logging.debug("Argument: " + arg)
            self._checkAndDetermineArgument(opt, arg)            
                
        self._validateArguments()
        self.logData()
        
        return self._inputfile, self._outputfile, self._dateformat, self._separatorMode, self._manufacturer, self._merchant

    def _checkAndDetermineArgument(self, opt, arg):
        if opt == '-h':
            raise HelpCalledException()
        if opt == "-i":
            self._inputfile = arg
        if opt == "-o":
            self._outputfile = arg
        if opt == "--manufacturer":
            self._manufacturer = arg
        if opt == "--merchant":
            self._merchant = arg
        if opt == "--separators":
            self._separatorMode = arg
        if opt == "--dateformat":
            self._dateformat = arg

    def _validateArguments(self):
        if self._inputfile is None:
            raise MissingArgumentException("Inputfile is missing.")
        if self._outputfile is None:
            raise MissingArgumentException("Outputfile is missing.")
        if self._dateformat is None:
            raise MissingArgumentException("Dateformat  is missing.")
        if self._separatorMode is None:
            raise MissingArgumentException("SeparateorMode  is missing.")

    def logData(self):
        logging.info("Input file is {0}".format(self._inputfile))
        logging.info("Output file is {0}".format(self._outputfile))
        if self._merchant is not None:
            logging.info("Merchant: {0}".format(self._merchant))
        if self._manufacturer is not None:
            logging.info("Manufacturer: {0}".format(self._manufacturer))
    

