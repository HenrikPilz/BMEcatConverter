from __future__ import print_function

import os
import sys
import logging
import getopt

import time

from argumentParser import ArgumentParser
from argumentParser import MissingArgumentException
from argumentParser import HelpCalledException
import packageInstaller
from converter import Converter
from converter import ConversionModeException

loggingLevel = logging.INFO

def printHelp():
    """
    Hilfe ausgeben
    """
    print("python main.py -i <inputfile> -o <outputfile> --dateformat \"%Y-%m-%d\" --separators english")
    print("\t--dateformat <dateformat>")
    print("\t\te.g. '%Y-%m-%d' or '%d.%m.%Y' or anything else with Y as Year, d as day and m as month ")
    print("\t--separators <english|german|detect>")
    print("\t\te.g. -separators german leads to numbers beeing expected like 10.000,00")
    print("\t\t     -separators english leads to numbers beeing expected like 10,000.00")
    print("\t\t     -separators detect tries to detect what could be there (unsafe).")
    print("Optionally:")
    print("\t--merchant <Merchantname>")
    print("\t--manufacturer <Manufacturername>")
    print("\ti.e. python main.py -i makita_bmecat.xml -o makita_excelfilname.xlsx -merchant \"Contorion\" -manufacturer \"Makita\"")


'''
    setUp Logging for File and Console
'''

def createFileLoggingHandler(logfilename, logLevel=logging.DEBUG, logFormat='%(levelname)7s: %(message)s'):
    if os.path.exists(logfilename):
        os.remove(logfilename)
    ''' log File'''
    logFileHandler = logging.FileHandler(filename=logfilename, mode='w')
    logFileFormatter = logging.Formatter(logFormat)
    logFileHandler.setFormatter(logFileFormatter)
    logFileHandler.setLevel(logLevel)
    return logFileHandler


def configureStdoutLogging():
    frmStdOut = logging.Formatter('%(levelname)7s - %(message)s')
    ''' Console out '''
    stdOutHandler = logging.StreamHandler(sys.stdout)
    stdOutHandler.setFormatter(frmStdOut)
    stdOutHandler.setLevel(loggingLevel)
    return stdOutHandler

def setUpLogging():
    logger = logging.getLogger()
    
    ''' Debug Log File '''
    debugLogFileHandler = createFileLoggingHandler(logfilename="convert_debug.log", logFormat='%(levelname)7s - [%(filename)20s:%(lineno)s - %(funcName)20s()]: %(message)s')
    logger.addHandler(debugLogFileHandler)

    ''' Common Log File for Validation etc.'''
    logFileHandler = createFileLoggingHandler(logfilename="convert.log", logLevel=logging.WARNING) 
    logger.addHandler(logFileHandler)
    
    stdOutHandler = configureStdoutLogging()
    logger.addHandler(stdOutHandler) 
    logger.setLevel(loggingLevel)
    
if __name__ == '__main__':
    # Check for openpyxl
    packageInstaller.installIfNeeded("openpyxl")
    packageInstaller.installIfNeeded("regex")
    packageInstaller.installIfNeeded("lxml")

    # Loging einstgellen: zwei Outputdateien plus Konsole 
    setUpLogging()

    logging.debug('Number of arguments:', len(sys.argv), 'arguments.')
    logging.debug('Argument List:', str(sys.argv))
    t1 = time.clock()
    
    try:
        argv = sys.argv[1:]
        inputFilename, outputFilename, dateFormat, separatorMode, manufacturerName, merchantName = ArgumentParser().parse(argv)
        converter = Converter(inputFilename, outputFilename, dateFormat, separatorMode, manufacturerName, merchantName)        
        converter.convert()
    except FileNotFoundError as fnfe:
        print("Dateiname konnte nicht gefunden werden: ", str(fnfe))
        sys.exit(5)
    except HelpCalledException:
        printHelp()
    except ConversionModeException as cme:
        print("Wrong Conversion Mode: ", str(cme))
        printHelp()
        sys.exit(2)
    except MissingArgumentException as mae:
        print("Missing Arguments: ", str(mae))
        printHelp()
        sys.exit(3)
    except getopt.GetoptError:
        print("Error: ")
        printHelp()
        sys.exit(4)
    
    t2 = time.clock()
    duration = t2-t1
    if duration < 60:
        print('Duration in seconds: ', (t2-t1))
    else:
        print('Duration in minutes: ', (t2-t1)/60)