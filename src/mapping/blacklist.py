'''
Created on 14.06.2017

@author: henrik.pilz
'''

import csv
import logging
import os


class Blacklist(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self._filename = filename
        self._blacklist = []
        self._readFileAndAddToList()

    def _addEntryToList(self, entry):
        self._blacklist.append(entry)
        logging.debug("Blacklistentry: '{v:s}'".format(v=entry))

    def _addRowToList(self, row):
        for entry in row:
            self._addEntryToList(entry)

    def _readRows(self, blacklistFile):
        for row in csv.reader(blacklistFile, delimiter=';'):
            self._addRowToList(row)

    def _readFileAndAddToList(self):
        if self._filename is not None:
            logging.debug(os.getcwd())
            logging.debug(self._filename)
            with open(self._filename, newline='', encoding='utf-8') as blacklistFile:
                self._readRows(blacklistFile)

    def contains(self, entry):
        return entry in self._blacklist
