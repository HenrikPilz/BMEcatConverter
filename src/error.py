'''
Created on 27.08.2018
module holding all exceptions raised

@author: Henrik Pilz
'''


class ConversionModeException(Exception):
    '''
    Exception for wrong converion modes
    '''


class HelpCalledException(Exception):
    '''
    Exception if Help is called
    '''


class MissingArgumentException(Exception):
    '''
    Exception if an argument is Missing
    '''


class SeparatorNotDetectableException(Exception):
    '''
    If the Separators are not detectable
    '''


class DataErrorException(Exception):
    '''
    Exception if the validation of an article fails.
    '''


class NoValueGivenException(DataErrorException):
    '''
    Exception thrown when no Value is given.
    '''


class DateFormatMissingException(DataErrorException):
    '''
    Exception if an argument is Missing
    '''


class FormulaFoundException(DataErrorException):
    '''
    Exception thrown if an excel formula entry is found.
    '''


class NumberFormatException(DataErrorException):
    '''
    If the format of the number is wrong
    '''
