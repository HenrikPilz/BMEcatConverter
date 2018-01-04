'''
Created on 14.06.2017

@author: henrik.pilz
'''

from _csv import QUOTE_NONE
from abc import abstractmethod
from csv import Dialect
import csv
import logging
import os


class rawCSV(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ';'
    quotechar = None
    doublequote = False
    skipinitialspace = False
    lineterminator = '\n'
    quoting = QUOTE_NONE


class CsvFile(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self._filename = filename
        self._readFile()

    @abstractmethod
    def _readRow(self, row):
        raise NotImplementedError("_readRow wurde nicht implementiert.")

    def _readRows(self, csvFile):
        for row in csv.reader(csvFile, dialect=rawCSV()):
            self._readRow(row)

    def _readFile(self):
        if self._filename is not None:
            logging.debug(os.getcwd())
            logging.debug(self._filename)
            with open(self._filename, encoding='utf-8') as csvFile:
                self._readRows(csvFile)
