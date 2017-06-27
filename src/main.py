from xml.sax import make_parser, handler
from importHandler.xml.bmecatHandler import BMEcatHandler as BMEcatImportHandler
'''from exportHandler.xml.bmecatHandler import BMEcatExportHandler'''
from exportHandler.excel.pyxelHandler import PyxelHandler
import logging
import sys
import os
import sys
import getopt
import time

loggingLevel = logging.WARNING

'''
Einstellungen für die zu erwartenden Daten:

 - Welches Datumsformat haben wir?
 - Welches Dezimaltrennzeichen wird genutzt?
 - Welches tausendertrennzeichen wird genutzt?
 
 Tausendertrennzeichen und Dezimalkennzeichen dürfen nicht gleich sein. 
'''
separators = { "german" : { "decimalSeparator" : ",", "thousandSeparator" : "." },
               "english" : { "decimalSeparator" : ".", "thousandSeparator" : "," }
             }

'''
    setUp Logging for File and Console
'''
def setUpLogging():
    logger = logging.getLogger()
    
    debugLogFilename = "convert_debug.log"
    if os.path.exists(debugLogFilename):
        os.remove(debugLogFilename)

    frmLogFile = logging.Formatter('%(levelname)7s - [%(filename)20s:%(lineno)s - %(funcName)20s()]: %(message)s')
    ''' Debug log File'''
    debugLogFileHandler = logging.FileHandler(filename=debugLogFilename )
    debugLogFileHandler.setFormatter(frmLogFile)
    debugLogFileHandler.setLevel(logging.DEBUG)

    logger.addHandler(debugLogFileHandler)

    commonLogFilename = "convert.log"
    if os.path.exists(commonLogFilename):
        os.remove(commonLogFilename)

    frmLogFile = logging.Formatter('%(levelname)7s: %(message)s')
    ''' Common Log File for Validation etc.'''
    logFileHandler = logging.FileHandler(filename=commonLogFilename )
    logFileHandler.setFormatter(frmLogFile)
    logFileHandler.setLevel(logging.WARNING)

    logger.addHandler(logFileHandler)
    
    frmStdOut = logging.Formatter('%(levelname)7s - %(message)s') 
    ''' Console out '''
    stdOutHandler = logging.StreamHandler(sys.stdout) 
    stdOutHandler.setFormatter(frmStdOut)
    stdOutHandler.setLevel(loggingLevel)

    logger.addHandler(stdOutHandler) 
    logger.setLevel(loggingLevel)
 
'''
convert XML BMEcat to Excel-File
'''
def xmlToExcel(bmecatFilename, excelFilename, dateFormat, separatorMode="detect", manufacturerName=None, merchant=None):
    parser = make_parser()
    
    decimalSeparator = separators[separatorMode]["decimalSeparator"]
    thousandSeparator = separators[separatorMode]["thousandSeparator"]

    
    importer = BMEcatImportHandler(dateFormat, decimalSeparator, thousandSeparator)
    parser.setContentHandler(importer)
    if bmecatFilename.startswith(".") or bmecatFilename.startswith(".."):
        bmecatFilename = os.getcwd() + "//" + bmecatFilename
    if excelFilename.startswith(".") or excelFilename.startswith(".."):
        excelFilename = os.getcwd() + "//" + excelFilename
    parser.parse("file:" + bmecatFilename)
    logging.info("Daten eingelesen")
    exporter = PyxelHandler(importer._articles, excelFilename, manufacturerName)
    logging.info("Erstelle Excel-Datei")
    exporter.createNewWorkbook()
    logging.info("Fertig.")
    
'''
convert Excel-File to XML BMEcat
'''
def excelToXml(inputPath, bmecatFilename):
    if inputPath is None or not os.inputPath.exists(inputPath):
        raise Exception("Kein gültiger Pfad angegeben.") 

    importer = ExcelImporter()
    articles = { "new" : [], "update" : [], "delete" : [] }
    if os.path.isfile(inputPath):
        importer.readWorkbook(inputPath)
        articles = importer._articles
    else:
        for filename in os.listdir(inputPath):
            importer.readWorkbook(os.path.join(inputPath,filename))
            for articleType in importer._articles.keys():
                if len(importer._articles[articleType]) > 0:
                    articles[articleType].extend(importer._articles[articleType]) 
    
    logging.info("Daten eingelesen")
    print("Daten eingelesen")
    
    exporter = BMEcatExportHandler(dateFormat, decimalSeparator, thousandSeparator, articles, bmecatFilename)
    
    logging.info("Erstelle Excel-Datei")
    print("Erstelle Excel-Datei")
    
    logging.info("Fertig.")
    print("Fertig.")

def determineArguments(argv):
    inputfile = None
    outputfile = None
    merchant = None
    manufacturer = None
    dateformat = None
    separatorMode = None
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:", ["merchant=", "manufacturer=", "dateformat=", "separators="])
        print("Options: ", opts)
    except getopt.GetoptError:
        print("Error: ")
        printHelp()
        sys.exit(2)

    for opt, arg in opts:
        print("Option: " + opt)
        print("Argument: " + arg)
        if opt == '-h':
            printHelp()
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

    if inputfile is None or outputfile is None or dateformat is None or separatorMode is None:
        printHelp()
    
    logging.info("Input file is {0}".format(inputfile))
    logging.info("Output file is {0}".format(outputfile))
    if merchant is not None:
        logging.info("Merchant: {0}".format(merchant))
    if manufacturer is not None:
        logging.info("Manufacturer: {0}".format(manufacturer))

    return inputfile, outputfile, merchant, manufacturer, dateformat, separatorMode

def printHelp():
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
    sys.exit()

def main(argv):
    setUpLogging()
    inputFilename, outputFilename, merchantName, manufacturerName, dateFormat, separatorMode = determineArguments(argv)
    xmlToExcel(inputFilename, outputFilename, dateFormat, separatorMode, manufacturerName, merchantName)
    
if __name__ == '__main__':
    logging.debug('Number of arguments:', len(sys.argv), 'arguments.')
    logging.debug('Argument List:', str(sys.argv))
    t1 = time.clock()
    main(sys.argv[1:])
    t2 = time.clock()
    print('Dauer: ', (t2-t1)/60)
