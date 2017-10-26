'''
Created on 01.09.2017

@author: henrik.pilz
'''
import logging
import os
import time
from xml.sax import make_parser

from exporter.excel import PyxelExporter
from exporter.xml import BMEcatExporter
from importer.excel import ExcelImporter
from importer.xml import BMEcatImportHandler
from resolver.dtdResolver import DTDResolver


class ConversionModeException(Exception):
    '''
    Exception for wrong converion modes
    '''

class Converter(object):
    '''
    classdocs
    '''

    # Tausendertrennzeichen und Dezimalkennzeichen dürfen nicht gleich sein. 
    separators = { "german" : { "decimalSeparator" : ",", "thousandSeparator" : "." },
                   "english" : { "decimalSeparator" : ".", "thousandSeparator" : "," }
                 }

    def __init__(self, inputfile, outputfile, dateFormat, separatorMode="detect", manufacturerName=None, merchant=None):
        '''
        Constructor
        '''
        self.inputfile=inputfile
        self.outputfile=outputfile
        self.dateFormat=dateFormat
        self.separatorMode=separatorMode
        self.manufacturerName=manufacturerName
        self.merchant=merchant
        
    def xmlToExcel(self):
        '''
        convert XML BMEcat to Excel-File
        '''
        parser = make_parser()
        
        decimalSeparator = self.separators[self.separatorMode]["decimalSeparator"]
        thousandSeparator = self.separators[self.separatorMode]["thousandSeparator"]
            
        importer = BMEcatImportHandler(self.dateFormat, decimalSeparator, thousandSeparator)
        parser.setContentHandler(importer)
        parser.setEntityResolver(DTDResolver())
        if self.inputfile.startswith(".") or self.inputfile.startswith(".."):
            self.inputfile = os.getcwd() + "//" + self.inputfile
        if self.outputfile.startswith(".") or self.outputfile.startswith(".."):
            self.outputfile = os.getcwd() + "//" + self.outputfile
        parser.parse("file:" + self.inputfile)
        logging.info("Daten eingelesen")
    
        exporter = PyxelExporter(importer.articles, self.outputfile, self.manufacturerName)
        logging.info("Erstelle Excel-Datei")
        exporter.createNewWorkbook()
        logging.info("Fertig.")
    
    def excelToXml(self):
        '''
        convert Excel-File to XML BMEcat
        '''

        importer = ExcelImporter()
        
        if os.path.isfile(self.inputfile):
            t1 = time.clock()
            importer.readWorkbook(self.inputfile)
            t2 = time.clock()
            print ("Einlesen:")
            self.computeDuration(t1, t2)
            
            articles = { 'new' : importer.articles }
        
            logging.info("Daten eingelesen")
            print("Daten eingelesen")
        
            exporter = BMEcatExporter(articles, self.outputfile)
        
            logging.info("Erstelle XML-Datei")
            print("Erstelle XML-Datei")
            t3 = time.clock()
            exporter.writeBMEcatAsXML()
            t4 = time.clock()
            print ("Wegschreiben:")
            self.computeDuration(t3, t4)
        else:
            raise FileNotFoundError("Datei '{0}' wurde nicht gefunden".format(self.inputfile))
        logging.info("Fertig.")
        print("Fertig.")
        
    def convert(self):
        if self.inputfile.endswith(".xml") and self.outputfile.endswith(".xlsx"):
            self.xmlToExcel()
        elif self.inputfile.endswith(".xlsx") and self.outputfile.endswith(".xml"):
            self.excelToXml()
        else:
            raise ConversionModeException("Mode not supported")
        
    def computeDuration(self, t1, t2):
        duration = t2-t1
        if duration < 60:
            print('Duration in seconds: ', (t2-t1))
        else:
            print('Duration in minutes: ', (t2-t1)/60)
