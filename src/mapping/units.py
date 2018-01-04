'''
Created on 13.06.2017

@author: henrik.pilz
'''

import logging

from mapping.csvfile import CsvFile


class UnitMapper(CsvFile):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self._units = {}
        super().__init__(filename)

    def _addEntryToMap(self, key, value=""):
        self._units[key] = value
        logging.debug("BMEcat Unit: '{k:s}' mapped to '{v:s}'".format(k=key, v=value))

    def _readRow(self, row):
        if len(row) == 0:
            return
        if len(row) == 1:
            self._addEntryToMap(row[0])
        elif len(row) == 2:
            self._addEntryToMap(row[0], row[1])
        else:
            logging.error("BMEcat Unit Fehler in der Einheitenzuordnung: '{r:s}'".format(r=str(row)))

    def hasKey(self, bmecatUnit):
        return bmecatUnit in list(self._units.keys())

    def getSIUnit(self, bmecatUnit):
        return self._units[bmecatUnit]
