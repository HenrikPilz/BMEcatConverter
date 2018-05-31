from __future__ import print_function

from urllib.error import URLError
import getopt
import logging
import os
import sys
import time

from argumentParser import ArgumentParser
from argumentParser import HelpCalledException
from argumentParser import MissingArgumentException
from converter import ConversionModeException
from converter import Converter
from exporter.xml import DataErrorException


def printHelp():
    """
    Hilfe ausgeben
    """
    logging.info("---  Help  ---\n\t  python main.py -i <inputfile> -o <outputfile>" +
                 " --dateformat \"%Y-%m-%d\" --separators english" +
                 "\n"
                 "\t  There are two modes in which the converter can be used:\n" +
                 "\t\t  1.\tInput XML and Output xlsx:\n" +
                 "\t  This means converting from any BMEcat format to Excel\n" +
                 "\t\t  --dateformat <dateformat>\n" +
                 "\t\t\t  e.g. '%Y-%m-%d' or '%d.%m.%Y' or anything else with Y as Year" +
                 ", d as day and m as month\n" +
                 "\t\t  --separators <english|german|detect>\n" +
                 "\t\t\t  e.g. -separators german leads to numbers" +
                 " beeing expected like 10.000,00\n" +
                 "\t\t\t       -separators english leads to numbers" +
                 " beeing expected like 10,000.00\n" +
                 "\t\t\t       -separators detect tries to detect" +
                 " what could be there (unsafe).\n" +
                 "\t  Optionally:\n" +
                 "\t\t  --merchant <Merchantname>\n" +
                 "\t\t  --manufacturer <Manufacturername>\n" +
                 "\t\t  i.e. python main.py -i makita_bmecat.xml" +
                 " -o makita_excelfilname.xlsx -merchant \"Contorion\"" +
                 " -manufacturer \"Makita\"\n")


def findNextFreeLogfilename(logfilename):
    for i in range(1, 11):
        freeLogfilename = "{0}_{1:02n}".format(logfilename, i)
        if not os.path.exists(freeLogfilename):
            return freeLogfilename


def createFileLoggingHandler(logfilename, logLevel=logging.DEBUG,
                             logFormat='%(levelname)7s: %(message)s'):
    '''
    setUp Logging for File
    '''
    if os.path.exists(logfilename):
        try:
            os.remove(logfilename)
        except Exception:
            logfilename = findNextFreeLogfilename(logfilename)

    logfilename += ".log"
    ''' log File'''
    logFileHandler = logging.FileHandler(filename=logfilename, mode='w')
    logFileFormatter = logging.Formatter(logFormat)
    logFileHandler.setFormatter(logFileFormatter)
    logFileHandler.setLevel(logLevel)
    return logFileHandler


def configureStdoutLogging(logLevel=logging.DEBUG):
    '''
    setUp Logging for Console
    '''
    frmStdOut = logging.Formatter('%(levelname)7s - %(message)s')
    ''' Console out '''
    stdOutHandler = logging.StreamHandler(sys.stdout)
    stdOutHandler.setFormatter(frmStdOut)
    stdOutHandler.setLevel(logLevel)
    return stdOutHandler


def setUpLogging():
    loggingLevel = logging.INFO
    '''
    setUp Logging for File and Console
    '''
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.flush()
        handler.close()

    # Debug Log File
    fmt = '%(levelname)7s - [%(filename)20s:%(lineno)s - %(funcName)20s()]: %(message)s'
    debugLogFileHandler = createFileLoggingHandler(
                                        logfilename="convert_debug",
                                        logFormat=fmt)
    logger.addHandler(debugLogFileHandler)

    ''' Common Log File for Validation etc.'''
    logFileHandler = createFileLoggingHandler(logfilename="convert",
                                              logLevel=logging.WARNING)
    logger.addHandler(logFileHandler)

    stdOutHandler = configureStdoutLogging()
    logger.addHandler(stdOutHandler)
    logger.setLevel(loggingLevel)


def printHelpAndExit(errorMessage=None, exitCode=None):
    printHelp()
    if errorMessage is not None:
        logging.error(errorMessage)
    if exitCode is not None:
        sys.exit(exitCode)


def main(argv):
    # Loging einstgellen: zwei Outputdateien plus Konsole
    setUpLogging()

    logging.debug('Number of arguments:', len(argv), 'arguments.')
    logging.debug('Argument List:', str(argv))

    t1 = time.clock()

    try:
        argumentParser = ArgumentParser()
        argumentParser.parse(argv)
        converter = Converter(argumentParser.getConfig())
        converter.convert()
    except HelpCalledException:
        printHelpAndExit()
    except (FileNotFoundError, URLError) as fnfe:
        printHelpAndExit("File not found: {0}".format(str(fnfe)), 5)
    except ConversionModeException as cme:
        printHelpAndExit("Wrong Conversion Mode: {0}".format(str(cme)), 2)
    except (MissingArgumentException, getopt.GetoptError) as mae:
        printHelpAndExit("Missing/Wrong Arguments: {0}".format(str(mae)), 3)
    except DataErrorException as dee:
        logging.error("{0}".format(str(dee)))
        sys.exit(7)
    except Exception as e:
        logging.exception("General Exception: {0}".format(str(e)))
        sys.exit(6)

    computeDuration(t1, time.clock())


def computeDuration(t1, t2):
    duration = t2 - t1
    if duration < 60:
        print('Duration in seconds: ', (t2 - t1))
    else:
        print('Duration in minutes: ', (t2 - t1) / 60)


if __name__ == '__main__':
    main(sys.argv[1:])
