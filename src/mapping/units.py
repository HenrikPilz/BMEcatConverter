'''
Created on 13.06.2017

@author: henrik.pilz
'''

from _csv import QUOTE_NONE
from csv import Dialect
import csv
import logging
import os


class units(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ';'
    quotechar = None
    doublequote = False
    skipinitialspace = False
    lineterminator = '\n'
    quoting = QUOTE_NONE


class UnitMapper(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self._filename = filename
        self._units = {}
        self._readFileAndAddToMap()

    def _addEntryToMap(self, key, value=""):
        self._units[key] = value
        logging.debug("BMEcat Unit: '{k:s}' mapped to '{v:s}'".format(k=key, v=value))

    def _addRowToMap(self, row):
        if len(row) == 0:
            return
        if len(row) == 1:
            self._addEntryToMap(row[0])
        elif len(row) == 2:
            self._addEntryToMap(row[0], row[1])
        else:
            logging.error("BMEcat Unit Fehler in der Einheitenzuordnung: '{r:s}'".format(r=str(row)))

    def _readRows(self, unitFile):
        for row in csv.reader(unitFile, dialect=units()):
            self._addRowToMap(row)

    def _readFileAndAddToMap(self):
        if self._filename is not None:
            logging.debug(os.getcwd())
            logging.debug(self._filename)
            with open(self._filename, newline='\n', encoding='utf-8') as unitFile:
                self._readRows(unitFile)

    def hasKey(self, bmecatUnit):
        return bmecatUnit in list(self._units.keys())

    def getSIUnit(self, bmecatUnit):
        return self._units[bmecatUnit]
