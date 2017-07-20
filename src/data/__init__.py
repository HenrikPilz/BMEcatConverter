from abc import abstractmethod
import logging


class ValidatingObject(object):
    '''
    Interface Class for a validating Object
    '''
    
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def validate(self, throwingException=False):
        raise NotImplementedError("Please implement 'validate' in your class '{0}".format(__file__))
    
    def logError(self, errMsg, raiseException=False):
        '''
         Taking an ErrorMessage, logging it and if wanted throwing an Exception
        '''
        logging.error(errMsg)
        if raiseException:
            raise Exception(errMsg)
