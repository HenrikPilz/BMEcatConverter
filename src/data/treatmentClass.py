'''
Created on 05.05.2017

@author: henrik.pilz
'''
import logging


class TreatmentClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.classType = None
        self.value = None
        
    def validate(self):
        if self.classType is None:
            logging.error("Es muss eine Klassifizierung angegeben werden.")
        if self.value is None:
            logging.info("Es wurde kein Wert zur Klassifizierung angegeben.")