'''
Created on 13.06.2017

@author: henrik.pilz
'''

import csv
import os
import logging

class UnitMapper(object):
    '''
    classdocs
    '''    

    def __init__(self):
        '''
        Constructor
        '''
        self.filename = None 
        self._units = {}
        
    def readFile(self):
        if self.filename:
            logging.debug(os.getcwd())
            logging.debug(self.filename)
            staplefile = csv.reader(open(self.filename, newline='', encoding='utf-8'), delimiter=';')    
            for row in staplefile:
                if len(row) < 2:
                    self._units[row[0]] = ""
                    logging.debug("BMEcat Unit: '{k:s}' mapped to '{v:s}'".format(k=row[0],v=""))
                else:
                    self._units[row[0]] = row[1]
                    logging.debug("BMEcat Unit: '{k:s}' mapped to '{v:s}'".format(k=row[0],v=row[1]))

    def hasKey(self, bmecatUnit):
        return bmecatUnit in list(self._units.keys())

    def getSIUnit(self, bmecatUnit):
        return self._units[bmecatUnit]
    
    
class BMEcatUnitMapper(UnitMapper):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.filename = ".//documents//BMEcat//version//BMEcatUnitMapping.csv"
        super().readFile()

class ETIMUnitMapper(UnitMapper):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.filename = ".//documents//BMEcat//version//ETIMUnitMapping.csv"
        super().readFile()
