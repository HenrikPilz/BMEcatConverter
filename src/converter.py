'''
Created on 01.09.2017

@author: henrik.pilz
'''
from xml.sax import make_parser
import logging
import os
import time

from exporter.excel import PyxelExporter
from exporter.xml import BMEcatExporter
from importer import BMEcatImportHandler
from importer import ExcelImporter
from resolver.dtdResolver import DTDResolver
from transformer import SeparatorTransformer


class ConversionModeException(Exception):
    '''
    Exception for wrong converion modes
    '''


class DateFormatMissingException(Exception):
    '''
    Exception if an argument is Missing
    '''


class Converter(object):
    '''
    classdocs
    '''

    allowedExcelFormats = [".xlsx", ".xlsm", ".xltx", ".xltm"]

    def __init__(self, config):
        '''
        Constructor
        '''
        self._inputfile = config['inputfile']
        self._outputfile = config['outputfile']
        self._dateFormat = config['dateFormat']
        self._manufacturerName = config['manufacturerName']
        self._merchant = config['merchant']
        self._separatorTransformer = SeparatorTransformer(config['separatorMode'])

    def _relativePathToAbsolutePath(self, filename):
        if filename.startswith(".") or filename.startswith(".."):
            filename = os.path.join(os.getcwd(), filename)
        return filename

    def xmlToExcel(self):
        '''
        convert XML BMEcat to Excel-File
        '''
        if self._dateFormat is None or len(self._dateFormat.strip()) == 0:
            raise DateFormatMissingException("Zum Konvertieren von XML in Excel muss ein Datumsformat angegeben werden.")

        parser = make_parser()

        importer = BMEcatImportHandler(self._dateFormat, self._separatorTransformer)
        parser.setContentHandler(importer)
        parser.setEntityResolver(DTDResolver())

        t1 = time.clock()
        parser.parse("file:" + self._inputfile)
        t2 = time.clock()
        print("Einlesen:")
        self.computeDuration(t1, t2)
        logging.info("Daten eingelesen")

        exporter = PyxelExporter(importer.articles, self._outputfile, self._manufacturerName)
        logging.info("Erstelle Excel-Datei")
        t3 = time.clock()
        exporter.createNewWorkbook()
        t4 = time.clock()
        print("Wegschreiben:")
        self.computeDuration(t3, t4)
        logging.info("Fertig.")

    def excelToXml(self):
        '''
        convert Excel-File to XML BMEcat
        '''

        importer = ExcelImporter(self._separatorTransformer)

        if os.path.isfile(self._inputfile):
            t1 = time.clock()
            importer.readWorkbook(self._inputfile)
            t2 = time.clock()
            print("Einlesen:")
            self.computeDuration(t1, t2)

            articles = { 'new' : importer.articles }

            logging.info("Daten eingelesen")
            print("Daten eingelesen")

            exporter = BMEcatExporter(articles, self._outputfile, self._merchant)

            logging.info("Erstelle XML-Datei")
            print("Erstelle XML-Datei")
            t3 = time.clock()
            exporter.writeBMEcatAsXML()
            t4 = time.clock()
            print("Wegschreiben:")
            self.computeDuration(t3, t4)
        else:
            raise FileNotFoundError("Datei '{0}' wurde nicht gefunden".format(self._inputfile))
        logging.info("Fertig.")
        print("Fertig.")

    def convert(self):
        self._inputfile = self._relativePathToAbsolutePath(self._inputfile)
        self._outputfile = self._relativePathToAbsolutePath(self._outputfile)
        if self._inputfile.endswith(".xml") and self._isExcel(self._outputfile):
            self.__runConverterMethod(self.xmlToExcel)
        elif self._isExcel(self._inputfile) and self._outputfile.endswith(".xml"):
            self.__runConverterMethod(self.excelToXml)
        else:
            raise ConversionModeException("Mode not supported")

    def __runConverterMethod(self, method):
        try:
            method()
        except Exception as e:
            if os.path.exists(self._outputfile):
                os.remove(self._outputfile)
            raise e

    def _isExcel(self, filename):
        return str(filename[-5:]) in self.allowedExcelFormats

    def computeDuration(self, t1, t2):
        duration = t2 - t1
        if duration < 60:
            print('Duration in seconds: ', (t2 - t1))
        else:
            print('Duration in minutes: ', (t2 - t1) / 60)
