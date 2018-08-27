'''
Created on 01.09.2017

Parses given arguments and option and converting them into a config object

@author: henrik.pilz
'''

import getopt
import logging
from error import HelpCalledException
from error import MissingArgumentException


class ArgumentParser():
    '''
    classdocs
    '''
    def __init__(self):
        self.inputfile = None
        self.outputfile = None
        self.validation = 'strict'
        self.manufacturer = None
        self.dateformat = None
        self.separatorMode = None

    def parse(self, argv):
        """
        parsing arguments

        @param argv: arguments and options
        """
        opts, _ = getopt.getopt(argv,
                                "hi:o:",
                                ["validation=",
                                 "manufacturer=",
                                 "dateformat=",
                                 "separators="])

        logging.debug("Options: %s", opts)

        for opt, arg in opts:
            logging.debug("Option: %s", opt)
            logging.debug("Argument: %s", arg)
            self._checkAndDetermineArgument(opt, arg)

        self._validateArguments()
        self._logData()

    def _checkAndDetermineArgument(self, opt, arg):
        """
        check for each argument and option

        @param opt: options
        @param args: arguments
        """
        self._checkIfHelpCalled(opt, arg)
        self._checkForArguments(opt, arg)
        self._checkForOptions(opt, arg)

    def _checkIfHelpCalled(self, opt, arg):
        """
        checks if the help option is called.
        If so, raise HelpCalledException

        @param opt: options
        @param args: arguments
        """
        if opt == '-h':
            raise HelpCalledException()

    def _checkForArguments(self, opt, arg):
        """
        check for arguments, inputfile and outputfile

        @param opt: options
        @param args: arguments
        """
        if opt == "-i":
            self.inputfile = arg
        if opt == "-o":
            self.outputfile = arg

    def _checkForOptions(self, opt, arg):
        """
        check for options, manufacturer, validation mode,
        separators and date format

        @param opt: options
        @param args: arguments
        """
        if opt == "--manufacturer":
            self.manufacturer = arg
        if opt == "--validation":
            self.validation = arg
        if opt == "--separators":
            self.separatorMode = arg
        if opt == "--dateformat":
            self.dateformat = arg

    def _validateArguments(self):
        """
        validate if all arguments needed are set
        """
        if self.inputfile is None:
            raise MissingArgumentException("Inputfile is missing.")
        if self.outputfile is None:
            raise MissingArgumentException("Outputfile is missing.")

    def _logData(self):
        """
        log current configuration
        """
        logging.info("Input file is %s", self.inputfile)
        logging.info("Output file is %s", self.outputfile)
        if self.validation is not None:
            logging.info("Validation: %s", self.validation)
        if self.manufacturer is not None:
            logging.info("Manufacturer: %s", self.manufacturer)

    def getConfig(self):
        """
        return arguments and options as configuration object
        """
        return {
            'inputfile' : self.inputfile,
            'outputfile' : self.outputfile,
            'dateFormat' : self.dateformat,
            'separatorMode' : self.separatorMode,
            'manufacturerName': self.manufacturer,
            'validation' : self.validation
        }
