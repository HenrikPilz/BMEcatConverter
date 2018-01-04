'''
Created on 14.06.2017

@author: henrik.pilz
'''

import logging

from mapping.csvfile import CsvFile


class Blacklist(CsvFile):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self._blacklist = []
        super().__init__(filename)

    def _addEntryToList(self, entry):
        self._blacklist.append(entry)
        logging.debug("Blacklistentry: '{v:s}'".format(v=entry))

    def _readRow(self, row):
        for entry in row:
            self._addEntryToList(entry)

    def contains(self, entry):
        return entry in self._blacklist
