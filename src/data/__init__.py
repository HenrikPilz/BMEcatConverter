import logging
from abc import abstractmethod

class ValidatingObject(object):
    '''
    Interface Class for a validating Object
    '''
    
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def validate(self, throwingException=False):
        raise NotImplementedError()
    
    def logError(self, errMsg, raiseException=False):
        '''
         Taking an ErrorMessage, logging it and if wanted throwing an Exception
        '''
        logging.error(errMsg)
        if raiseException:
            raise Exception(errMsg)
