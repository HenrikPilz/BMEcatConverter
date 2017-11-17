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
from transformer.Separators import SeparatorTransformer


class ConversionModeException( Exception ):
    '''
    Exception for wrong converion modes
    '''

class Converter( object ):
    '''
    classdocs
    '''

    def __init__( self, config ):
        '''
        Constructor
        '''
        self._inputfile = config['inputfile']
        self._outputfile = config['outputfile']
        self._dateFormat = config['dateFormat']
        self._manufacturerName = config['manufacturerName']
        self._merchant = config['merchant']
        self._separatorTransformer = SeparatorTransformer( config['separatorMode'] )

    def xmlToExcel( self ):
        '''
        convert XML BMEcat to Excel-File
        '''
        parser = make_parser()

        importer = BMEcatImportHandler( self._dateFormat, self._separatorTransformer )
        parser.setContentHandler( importer )
        parser.setEntityResolver( DTDResolver() )
        if self._inputfile.startswith( "." ) or self._inputfile.startswith( ".." ):
            self._inputfile = os.getcwd() + "//" + self._inputfile
        if self._outputfile.startswith( "." ) or self._outputfile.startswith( ".." ):
            self._outputfile = os.getcwd() + "//" + self._outputfile
        t1 = time.clock()
        parser.parse( "file:" + self._inputfile )
        t2 = time.clock()
        print ( "Einlesen:" )
        self.computeDuration( t1, t2 )
        logging.info( "Daten eingelesen" )

        exporter = PyxelExporter( importer.articles, self._outputfile, self._manufacturerName )
        logging.info( "Erstelle Excel-Datei" )
        t3 = time.clock()
        exporter.createNewWorkbook()
        t4 = time.clock()
        print ( "Wegschreiben:" )
        self.computeDuration( t3, t4 )
        logging.info( "Fertig." )

    def excelToXml( self ):
        '''
        convert Excel-File to XML BMEcat
        '''

        importer = ExcelImporter( self._separatorTransformer )

        if os.path.isfile( self._inputfile ):
            t1 = time.clock()
            importer.readWorkbook( self._inputfile )
            t2 = time.clock()
            print ( "Einlesen:" )
            self.computeDuration( t1, t2 )

            articles = { 'new' : importer.articles }

            logging.info( "Daten eingelesen" )
            print( "Daten eingelesen" )

            exporter = BMEcatExporter( articles, self._outputfile, self._merchant )

            logging.info( "Erstelle XML-Datei" )
            print( "Erstelle XML-Datei" )
            t3 = time.clock()
            exporter.writeBMEcatAsXML()
            t4 = time.clock()
            print ( "Wegschreiben:" )
            self.computeDuration( t3, t4 )
        else:
            raise FileNotFoundError( "Datei '{0}' wurde nicht gefunden".format( self._inputfile ) )
        logging.info( "Fertig." )
        print( "Fertig." )

    def convert( self ):
        if self._inputfile.endswith( ".xml" ) and self._outputfile.endswith( ".xlsx" ):
            self.xmlToExcel()
        elif self._inputfile.endswith( ".xlsx" ) and self._outputfile.endswith( ".xml" ):
            self.excelToXml()
        else:
            raise ConversionModeException( "Mode not supported" )

    def computeDuration( self, t1, t2 ):
        duration = t2 - t1
        if duration < 60:
            print( 'Duration in seconds: ', ( t2 - t1 ) )
        else:
            print( 'Duration in minutes: ', ( t2 - t1 ) / 60 )
