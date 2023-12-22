"""
Created on 01.09.2017

@author: henrik.pilz
"""
from xml.sax import make_parser, handler
import logging
import os
import time
import urllib.error

from error import ConversionModeException
from error import DateFormatMissingException
from exporter import BMEcatExporter
from exporter import PyxelExporter
from importer import BMEcatImportHandler
from importer import ExcelImporter
from resolver import DTDResolver
from transformer import SeparatorTransformer


class Converter(object):
    """
    Converter for formats stated in allowedExcelFormats

    Attributes
    ----------
    allowedExcelFormats: Array
        formats of Excel, which can be handled
    """

    allowedExcelFormats = [".xlsx", ".xlsm", ".xltx", ".xltm"]

    def __init__(self, config):
        """
        Constructor
        """
        self._inputfile = config['inputfile']
        self._outputfile = config['outputfile']
        self._dateFormat = config['dateFormat']
        self._manufacturerName = config['manufacturerName']
        self._validation = config['validation']
        self._separatorTransformer = SeparatorTransformer(config['separatorMode'])

    def _relativePathToAbsolutePath(self, filename):
        if filename.startswith(".") or filename.startswith(".."):
            filename = os.path.join(os.getcwd(), filename)
        return filename

    def xmlToExcel(self):
        """
        convert XML BMEcat to Excel-File
        """
        if self._dateFormat is None or len(self._dateFormat.strip()) == 0:
            raise DateFormatMissingException("Zum Konvertieren von XML in Excel muss ein Datumsformat angegeben werden.")

        parser = make_parser()
        importer = BMEcatImportHandler(self._dateFormat, self._separatorTransformer)
        parser.setContentHandler(importer)
        parser.setEntityResolver(DTDResolver())

        t1 = time.time()
        try:
            parser.parse("file:" + self._inputfile)
        except urllib.error.URLError as urlError:
            raise FileNotFoundError(urlError)
        t2 = time.time()
        print("Einlesen:")
        self.__computeDuration(t1, t2)
        logging.info("Daten eingelesen")

        exporter = PyxelExporter(importer.articles, self._outputfile, self._manufacturerName)
        logging.info("Erstelle Excel-Datei")
        t3 = time.time()
        exporter.createNewWorkbook()
        t4 = time.time()
        print("Wegschreiben:")
        self.__computeDuration(t3, t4)
        logging.info("Fertig.")

    def excelToXml(self):
        """
        convert Excel-File to XML BMEcat
        """

        importer = ExcelImporter(self._separatorTransformer)

        if os.path.isfile(self._inputfile):
            t1 = time.time()
            importer.readWorkbook(self._inputfile)
            t2 = time.time()
            print("Einlesen:")
            self.__computeDuration(t1, t2)

            articles = { 'new' : importer.articles }

            logging.info("Daten eingelesen")
            print("Daten eingelesen")

            exporter = BMEcatExporter(articles, self._outputfile, self._validation)

            logging.info("Erstelle XML-Datei")
            print("Erstelle XML-Datei")
            t3 = time.time()
            exporter.writeBMEcatAsXML()
            t4 = time.time()
            print("Wegschreiben:")
            self.__computeDuration(t3, t4)
        else:
            raise FileNotFoundError("Datei '{0}' wurde nicht gefunden".format(self._inputfile))
        logging.info("Fertig.")
        print("Fertig.")

    def convert(self):
        """
        convert from input to output
        """
        self._inputfile = self._relativePathToAbsolutePath(self._inputfile)
        self._outputfile = self._relativePathToAbsolutePath(self._outputfile)
        if self._inputfile.endswith(".xml") and self.__isExcel(self._outputfile):
            self.__runConverterMethod(self.xmlToExcel)
        elif self.__isExcel(self._inputfile) and self._outputfile.endswith(".xml"):
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

    def __isExcel(self, filename):
        return str(filename[-5:]) in self.allowedExcelFormats

    def __computeDuration(self, t1, t2):
        duration = t2 - t1
        if duration < 60:
            print('Duration in seconds: ', (t2 - t1))
        else:
            print('Duration in minutes: ', (t2 - t1) / 60)
