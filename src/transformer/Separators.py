'''
Created on 26.06.2017

@author: henrik.pilz
'''

import logging

class SeparatorNotDetectableException(Exception):
    '''
    If the Separators are not detectable
    '''


class NumberFormatException(Exception):
    '''
    If the format of the number is wrong
    '''


class SeparatorTransformer(object):
    '''
    classdocs
    '''

    '''
    Einstellungen für die zu erwartenden Daten:
    
     - Welches Datumsformat haben wir?
     - Welches Dezimaltrennzeichen wird genutzt?
     - Welches tausendertrennzeichen wird genutzt?
     
     Tausendertrennzeichen und Dezimalkennzeichen dürfen nicht gleich sein.     
    '''
    _comma = ","
    _dot = "."

    _separators = { 
                    "german" : {
                                "decimalSeparator" : _comma,
                                "thousandSeparator" :_dot
                                },
                    "english" : { 
                                "decimalSeparator" : _dot,
                                "thousandSeparator" : _comma
                                }
                 }
    
    _destinationEncoding = "english"


    def _setSeparators(self, sourceEncoding):
        self._decimalSeparator = self._separators[sourceEncoding]["decimalSeparator"]
        self._thousandSeparator = self._separators[sourceEncoding]["thousandSeparator"]

    def __init__(self, sourceEncoding="detect"):
        '''
        Constructor
        @param mode Welchen Input haben wir?
        '''
        if sourceEncoding in self._separators.keys():
            self._setSeparators(sourceEncoding)
        else:
            self._decimalSeparator = None
            self._thousandSeparator = None
            
    def transform(self, value):
        '''
        transformiert vom gegebenen Ausgangsmodus in die englische Dezimalversion.
        '''
        if self._decimalSeparator is None:
            self._autodetectSeparators(value)
        
        convertedString = value 
        if convertedString is not None:
            convertedString = str(convertedString).strip()
        
        if self._decimalSeparator is not None:
            self._checkOccurenceOfSeparatorsForSelectedMode(convertedString)
            convertedString = convertedString.replace(self._decimalSeparator,";")
            convertedString = convertedString.replace(self._thousandSeparator,"")
            convertedString = convertedString.replace(";", self._separators[self._destinationEncoding]["decimalSeparator"], 1)
            logging.debug("'{0}'".format(convertedString))
        
        if convertedString is not None and len(convertedString) > 0 :
            return float(convertedString)
        else:
            return None
        
    def _checkOccurenceOfSeparatorsForSelectedMode(self, stringValue):
        countDecimal = stringValue.count(self._decimalSeparator)
        firstIndexThousand = stringValue.find(self._thousandSeparator)
        firstIndexDecimal = stringValue.find(self._decimalSeparator)
        lastIndexThousand = stringValue.rfind(self._thousandSeparator)
        lastIndexDecimal = stringValue.rfind(self._decimalSeparator)
        
        if firstIndexDecimal < lastIndexThousand or countDecimal > 1 or \
            firstIndexThousand > firstIndexDecimal or \
            lastIndexThousand > -1 and (lastIndexDecimal - lastIndexThousand) % 4 != 0 or \
            firstIndexDecimal == -1 and firstIndexThousand > -1 and (lastIndexThousand != len(stringValue) - 4 ):
            raise NumberFormatException("Das Format '{0}' stimmmt nicht mit den gewählten Separatoren überein.".format(stringValue))



    def _checkOccurenceOfSeparatorsForAutoDetect(self, stringValue, countComma, countDot):
        firstIndexDot = stringValue.find(self._dot)
        firstIndexComma = stringValue.find(self._comma)
        lastIndexDot = stringValue.rfind(self._dot)
        lastIndexComma = stringValue.rfind(self._comma)

        if (firstIndexComma < firstIndexDot and firstIndexDot < lastIndexComma) or (firstIndexDot < firstIndexComma and firstIndexComma < lastIndexDot):
            raise SeparatorNotDetectableException("Could not detect Separators.")

        distanceCountMin = abs(firstIndexComma - firstIndexDot)
        distanceCountMax = abs(firstIndexComma - lastIndexDot)

        if countComma > 0 and countDot > 0 and (distanceCountMin % 4 != 0 or distanceCountMax % 4 != 0):
            raise SeparatorNotDetectableException("Could not detect Separators.")
        
        return lastIndexDot, lastIndexComma

    def _autodetectSeparators(self, value):
            stringValue = str(value)
            countDot = stringValue.count(self._dot)
            countComma = stringValue.count(self._comma)
            
            if (countDot > 1 and countComma == 0) or (countDot == 0 and countComma > 1) or (countDot > 1 and countComma > 1):
                message = "'{0}' and '{1}' occur multiple times each in the value '{2}'.".format(self._dot, self._comma, value)
            else:
                message = "Could not detect Separators."

            lastIndexDot, lastIndexComma = self._checkOccurenceOfSeparatorsForAutoDetect(stringValue, countComma, countDot)

            if countDot == 1 and countComma != 1:
                self._setSeparators("english")
            elif countComma == 1 and countDot != 1:
                self._setSeparators("german")
            elif countComma == 1 and countDot == 1:
                if lastIndexComma > lastIndexDot:
                    self._setSeparators("german")
                else:
                    self._setSeparators("english")
            elif countDot == 0 and countComma == 0:
                pass
            else:
                raise SeparatorNotDetectableException(message)
