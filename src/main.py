"""
Main class from where the BMEcatConverter is started.
"""
from __future__ import print_function

import getopt
import logging
import os
import sys
import time

from argumentParser import ArgumentParser
from converter import Converter
from error import ConversionModeException
from error import DataErrorException
from error import HelpCalledException
from error import MissingArgumentException


def printHelp():
    """
    Hilfe ausgeben
    """
    logging.info("### Help ###\n\n   ### Usage ###\n" +
                 "   The BMEcat-Converter has to be used with the following " +
                 "arguments:\n\n\t-i \"%path_to_inputfile%\"\n" +
                 "\tthis can be a relative or absolute path, it has to be " +
                 "either an Excelfile (*.xlsm or *.xlsx) or a BMEcat-file " +
                 "(*.xml).\n\t-o \"%path_to_outputfile%\"\n" +
                 "\tthis can be a relative or absolute path, it has to be " +
                 "either an Excelfile (*.xlsm or *.xlsx) or a BMEcat-file " +
                 "(*.xml).\n\t--dateformat=\"%Y-%m-%d\"\n" +
                 "\tthe dateformat has to be provided, if you convert from " +
                 "XML to Excel (Case one). You can usually derive the " +
                 "dateformat from the generation date of the BMEcat. If you " +
                 "use a cmd-file for running the converter you should escape" +
                 " the percentage sign by double-typing, i.e., " +
                 "\"%%Y-%%m-%%d\".\n\n" +
                 "   Thus with calling 'python src/main.py -i " +
                 "\"%path_to_inputfile%\" -o \"%path_to_outputfile%\"' " +
                 "will work if you convert from an Excelfile to a BMEcat.\n\n" +
                 "   The following options are set to default values:\n\n" +
                 "\t--dateformat=None\n\t--validation=\"strict\"\n" +
                 "\tDefault validation dissolves to 'strict', this means if a " +
                 "validation fails, an exception is raised and the conversion" +
                 " fails.\n" +
                 "\t--manufacturer=None\n\tDefault Manufacturer if no " +
                 "manufacturername is provided in the BMEcat.\n" +
                 "\t--separators=autodetect\n" +
                 "\tDefault is 'autodetect', which tries to resolve the " +
                 "thousands- and decimalseparator\n\n" +
                 "   ### Additional options ###\n" +
                 "   The options can be changed as follows:\n\n" +
                 "\t--dateformat=\"%Y-%m-%d\"\n" +
                 "\thas to be set if the generation date looks like " +
                 "\"2018-9-18\".\n" +
                 "\t%Y is the year with century, i.e., 2018\n" +
                 "\t%y is the year without century, i.e., 98 for 1998, 01 " +
                 "for 2001\n\t%m is the month\n\t%d is the day of the month\n" +
                 "\t%h is the hour\n\t%M is the minute\n\t%S is the second\n" +
                 "\t--validation=\"strict\"\n" +
                 "\tIn order to loosen the validationrules one could set a " +
                 "merchant with the option '--validation=\"strict\"'.\n" +
                 "\t'strict' means if an validation fails, an exception is " +
                 "raised and the conversion fails.\n" +
                 "\t'anything_else' only writes warnings but will create a " +
                 "BMEcat if nothing really bad is inserted.\n" +
                 "\t--manufacturer\n" +
                 "\t--separators=autodetect\n\tthree states are possible\n" +
                 "\t- autodetect:\n" +
                 "\t\ttries to autodetect thousands- and decimalseparators\n" +
                 "\t- english:\n" +
                 "\t\tset thousandsseparator to comma and decimalseparator " +
                 "to dot.\n" +
                 "\t- german:\n" +
                 "\t\tset thousandsseparator to dot and decimalseparator " +
                 "to comma.\n\n")


def findNextFreeLogfilename(logfilename):
    """
    if logfile is already used, open a new one
    """
    for i in range(1, 11):
        freeLogfilename = "{0}_{1:02n}".format(logfilename, i)
        if not os.path.exists(freeLogfilename):
            return freeLogfilename


def createFileLoggingHandler(logfilename, logLevel=logging.DEBUG, logFormat='%(levelname)7s: %(message)s'):
    """
    setUp Logging for File
    """
    if os.path.exists(logfilename):
        try:
            os.remove(logfilename)
        except Exception:
            logfilename = findNextFreeLogfilename(logfilename)

    logfilename += ".log"
    # log File
    logFileHandler = logging.FileHandler(filename=logfilename, mode='w')
    logFileFormatter = logging.Formatter(logFormat)
    logFileHandler.setFormatter(logFileFormatter)
    logFileHandler.setLevel(logLevel)
    return logFileHandler


def configureStdoutLogging(logLevel=logging.DEBUG):
    """
    setUp Logging for Console
    """
    frmStdOut = logging.Formatter('%(levelname)7s - %(message)s')
    # Console out
    stdOutHandler = logging.StreamHandler(sys.stdout)
    stdOutHandler.setFormatter(frmStdOut)
    stdOutHandler.setLevel(logLevel)
    return stdOutHandler


def setUpLogging():
    """
    setUp Logging for File and Console
    """
    loggingLevel = logging.INFO
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.flush()
        handler.close()

    # Debug Log File
    fmt = '%(levelname)7s - [%(filename)20s:%(lineno)s - %(funcName)20s()]: %(message)s'
    debugLogFileHandler = createFileLoggingHandler(logfilename="convert_debug",
                                                   logFormat=fmt)
    logger.addHandler(debugLogFileHandler)

    # Common Log File for Validation etc.
    logFileHandler = createFileLoggingHandler(logfilename="convert",
                                              logLevel=logging.WARNING)
    logger.addHandler(logFileHandler)

    stdOutHandler = configureStdoutLogging()
    logger.addHandler(stdOutHandler)
    logger.setLevel(loggingLevel)


def printHelpAndExit(errorMessage=None, exitCode=None):
    """
    print help and exit with exit code and/or error message
    """
    printHelp()
    if errorMessage is not None:
        logging.error(errorMessage)
    if exitCode is not None:
        sys.exit(exitCode)


def main(argv):
    """
    main method
    """
    # Loging einstellen: zwei Output-dateien plus Konsole
    setUpLogging()

    logging.debug('Number of arguments: %d arguments.', len(argv))
    logging.debug('Argument List: %s', str(argv))

    startingTime = time.time()

    try:
        argumentParser = ArgumentParser()
        argumentParser.parse(argv)
        converter = Converter(argumentParser.getConfig())
        converter.convert()
    except HelpCalledException:
        printHelpAndExit()
    except FileNotFoundError as fnfe:
        printHelpAndExit("File not found: {0}".format(str(fnfe)), 5)
    except ConversionModeException as cme:
        printHelpAndExit("Wrong Conversion Mode: {0}".format(str(cme)), 2)
    except (MissingArgumentException, getopt.GetoptError) as mae:
        printHelpAndExit("Missing/Wrong Arguments: {0}".format(str(mae)), 3)
    except DataErrorException as dee:
        logging.error(str(dee))
        sys.exit(7)
    except Exception as generalException:
        logging.exception("General Exception: %s", str(generalException))
        sys.exit(6)

    computeDuration(startingTime)


def computeDuration(beginning):
    """
    compute duration from beginning to end.
    """
    duration = time.time() - beginning
    if duration < 60:
        print('Duration in seconds: %d', duration)
    else:
        print('Duration in minutes: %d', duration / 60)


if __name__ == '__main__':
    main(sys.argv[1:])
