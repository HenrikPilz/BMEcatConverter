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
        self.filename = filename
        self._units = {}
        if self.filename is not None:
            self.readFile()

    def readFile(self):
        if self.filename:
            logging.debug(os.getcwd())
            logging.debug(self.filename)
            staplefile = csv.reader(open(self.filename, newline='\n', encoding='utf-8'), dialect=units())
            for row in staplefile:
                if len(row) < 2:
                    self._units[row[0]] = ""
                    logging.debug("BMEcat Unit: '{k:s}' mapped to '{v:s}'".format(k=row[0], v=""))
                else:
                    self._units[row[0]] = row[1]
                    logging.debug("BMEcat Unit: '{k:s}' mapped to '{v:s}'".format(k=row[0], v=row[1]))

    def hasKey(self, bmecatUnit):
        return bmecatUnit in list(self._units.keys())

    def getSIUnit(self, bmecatUnit):
        return self._units[bmecatUnit]
