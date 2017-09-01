'''
Created on 01.09.2017

@author: henrik.pilz
'''

import getopt
import logging

class MissingArgumentException(Exception):
    '''
    Exception if an argument is Missing
    '''

class ArgumentParser():
    '''
    classdocs
    '''

    @classmethod
    def parse(self, argv):
        inputfile = None
        outputfile = None
        merchant = None
        manufacturer = None
        dateformat = None
        separatorMode = None
        
        opts, args = getopt.getopt(argv,"hi:o:", ["merchant=", "manufacturer=", "dateformat=", "separators="])
        print("Options: ", opts)
    
        for opt, arg in opts:
            print("Option: " + opt)
            print("Argument: " + arg)
            if opt == '-h':
                ArgumentParser.printHelp()
            elif opt == "-i":
                inputfile = arg
            elif opt == "-o":
                outputfile = arg
            elif opt == "--manufacturer":
                manufacturer = arg
            elif opt == "--merchant":
                merchant = arg
            elif opt == "--separators":
                separatorMode = arg
            elif opt == "--dateformat":
                dateformat=arg            
    
        if inputfile is None:
            raise MissingArgumentException("Inputfile is missing.")
        if outputfile is None:
            raise MissingArgumentException("Outputfile is missing.")
        if dateformat is None:
            raise MissingArgumentException("Dateformat  is missing.")
        if separatorMode is None:
            raise MissingArgumentException("SeparateorMode  is missing.")


        logging.info("Input file is {0}".format(inputfile))
        logging.info("Output file is {0}".format(outputfile))
        if merchant is not None:
            logging.info("Merchant: {0}".format(merchant))
        if manufacturer is not None:
            logging.info("Manufacturer: {0}".format(manufacturer))
    
        return inputfile, outputfile, dateformat, separatorMode, manufacturer, merchant
