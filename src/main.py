from xml.sax import make_parser, handler
from importHandler.xml.bmecatHandler import BMEcatHandler as BMEcatImportHandler
'''from exportHandler.xml.bmecatHandler import BMEcatExportHandler'''
from exportHandler.excel.pyxelHandler import PyxelHandler
import logging
import sys
import os

'''
Einstellungen für die zu erwartenden Daten:

 - Welches Datumsformat haben wir?
 - Welches Dezimaltrennzeichen wird genutzt?
 - Welches tausendertrennzeichen wird genutzt?
 
 Tausendertrennzeichen und Dezimalkennzeichen dürfen nicht gleich sein. 
'''

''' Für ein Datum: 2017-05-31 '''
dateFormat="%Y-%m-%d"
''' Für ein Datum: 05.31.2017 '''
'''dateFormat="%d.%m.%Y"'''
''' Andere Varianten sind entsprechend erstellbar'''

decimalSeparator = "."
thousandSeparator = ","


'''
Merchant für den der BMEcat erstellet werden soll.

'''
merchantName = "Contorion"
'''
Hersteller für den der BMEcat konvertiert werden soll.

'''
manufacturerName = None


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
    stdOutHandler.setLevel(logging.WARNING)

    logger.addHandler(stdOutHandler) 
    logger.setLevel(logging.INFO)
 
'''
convert XML BMEcat to Excel-File
'''
def xmlToExcel(bmecatFilename, excelFilename):
    parser = make_parser()
    
    dateFormat="%Y-%m-%d"
    '''
    dateFormat="%d.%m.%Y"'''
    decimalSeparator = "."
    thousandSeparator = ","

    
    importer = BMEcatImportHandler(dateFormat, decimalSeparator, thousandSeparator)
    parser.setContentHandler(importer)
    parser.parse(bmecatFilename)
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


def main():    
    setUpLogging()
    ''' Dateiname des BMEcats ohne Endung'''
    filename = "20170612_BMECat_ETIM6_Klartext_Kundenpreis_MAK"
    ''' Pfad wo der BMEcat liegt'''
    '''bmecatPath = "file:C://Users//henrik.pilz//My Documents//LiClipse Workspace//BMEcatConverter//documents//BMEcat//"'''
    bmecatPath = "file:C://Users//henrik.pilz//Desktop//Makita"

    if not bmecatPath.endswith("//"):
        bmecatPath += "//"
    xmlToExcel(bmecatPath + filename + ".xml", filename + ".xlsx")
    
if __name__ == '__main__':
    main()