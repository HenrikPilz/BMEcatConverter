'''
Created on 17.05.2017

@author: henrik.pilz
'''
import logging

class Variant(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.value = None
        self.productIdSuffix = None
       
    def validate(self):
        if self.value is None:
            logging.error("Die Variante wurde nicht definitiert.")
        if self.value is None:
            logging.error("Das Suffix für die Variante " + self.value + " wurde nicht definiert.")
