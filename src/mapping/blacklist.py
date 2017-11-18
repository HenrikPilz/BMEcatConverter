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
        self.filename = filename
        self._blacklist = []
        if self.filename is not None:
            self.readFile()

    def readFile(self):
        if self.filename:
            logging.debug(os.getcwd())
            logging.debug(self.filename)
            staplefile = csv.reader(open(self.filename, newline='', encoding='utf-8'), delimiter=';')
            for row in staplefile:
                if len(row) < 2:
                    self._blacklist.append(row[0])
                    logging.debug("Blacklistentry: '{v:s}'".format(v=row[0]))
                else:
                    for entry in row:
                        self._blacklist.append(entry)
                        logging.debug("Blacklistentry: '{v:s}'".format(v=entry))

    def contains(self, entry):
        return entry in self._blacklist
