'''
Created on 22.12.2023

@author: henrik.pilz
'''
from array import array
import logging
from datamodel import ValidatingObject


def noValidatingObject(elementToCheck, msg: str, raiseException = True):
    if not isinstance(elementToCheck, ValidatingObject):
        if raiseException:
            raise Exception(msg)
        logging.warning(msg)
        return True
    return False


def objectIsNone(objectToCheck, msg: str, raiseException = True):
    if objectToCheck is None:
        return True
    if raiseException:
        raise Exception(msg)
    logging.warning(msg)
    return False


def objectIsNotNone(objectToCheck, msg: str, raiseException = True):
    if objectToCheck is not None:
        return True
    if raiseException:
        raise Exception(msg)
    logging.warning(msg)
    return False


def objectIsNotNoneAndNotEmpty(objectToCheck, msg: str, raiseException = True):
    if objectIsNotNone(objectToCheck, msg, raiseException) and \
       isinstance(objectToCheck, (list, array, str)) and \
       len(objectToCheck) > 0:
        return True
    if raiseException:
        raise Exception(msg)
    logging.warning(msg)
    return False
