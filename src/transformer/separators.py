'''
Created on 26.06.2017

@author: henrik.pilz
'''

import logging

from error import NumberFormatException
from error import SeparatorNotDetectableException


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
                                "thousandSeparator" : _dot },
                    "english" : {
                                "decimalSeparator" : _dot,
                                "thousandSeparator" : _comma }
                 }

    _destinationEncoding = "english"

    def __init__(self, sourceEncoding="detect"):
        '''
        Constructor
        @param mode Welchen Input haben wir?
        '''
        self._setSeparators(sourceEncoding)

    def _setSeparators(self, sourceEncoding):
        if sourceEncoding in self._separators.keys():
            self._decimalSeparator = self._separators[sourceEncoding]["decimalSeparator"]
            self._thousandSeparator = self._separators[sourceEncoding]["thousandSeparator"]
        else:
            logging.warning("Das Erkennen des Dezimaltrennzeichens und des Tausendertrennzeichens wurde nicht übergeben und wird automatisch ermittelt." +
                            " Dies kann zu Problemen führen.")
            self._decimalSeparator = None
            self._thousandSeparator = None

    def transform(self, value):
        if value is None:
            return None

        convertedToString = str(value).strip(" \t\n\r")

        if len(convertedToString) == 0:
            return None

        '''
        transformiert vom gegebenen Ausgangsmodus in die englische Dezimalversion.
        '''
        if self._decimalSeparator is None:
            self._autodetectSeparators(convertedToString)

        # Warum hier kein else? Es kann sein, dass die Trennzeichen nicht erkannt wurden.
        if self._decimalSeparator is not None:
            self._checkOccurenceOfSeparators(convertedToString)
            convertedToString = self._convertSeparators(convertedToString)

        return self._returnCorrectNumberType(convertedToString)

    def _convertSeparators(self, value):
        value = value.replace(self._decimalSeparator, ";")
        value = value.replace(self._thousandSeparator, "")
        value = value.replace(";", self._separators[self._destinationEncoding]["decimalSeparator"], 1)
        logging.debug("'{0}'".format(value))
        return value

    def _returnCorrectNumberType(self, value):
        try:
            return int(value)
        except ValueError:
            return float(value)

    def _autodetectSeparators(self, value):
        stringValue = str(value)
        countComma = stringValue.count(self._comma)
        countDot = stringValue.count(self._dot)

        if countComma == 0 and countDot == 0:
            return
        elif countComma == 1 and countDot == 0:
            self._setSeparators("german")
        elif countComma == 0 and countDot == 1:
            self._setSeparators("english")
        else:
            self.__tryVariants(stringValue)

    def __tryVariants(self, value):
        failed = True
        for variant in self._separators.keys():
            try:
                self._setSeparators(variant)
                self._checkOccurenceOfSeparators(value)
            except (NumberFormatException, SeparatorNotDetectableException):
                continue
            failed = False
            break

        if failed:
            raise SeparatorNotDetectableException("Could not detect Separators for value '{0}'.".format(value))

    def _checkOccurenceOfSeparators(self, stringValue):
        decimalGroups = stringValue.split(self._decimalSeparator)
        self._checkDecimalSeparator(stringValue, decimalGroups)

        thousandGroups = decimalGroups[0].split(self._thousandSeparator)

        if len(thousandGroups[0]) not in [1, 2, 3] and len(thousandGroups) > 1:
            raise NumberFormatException("Thousandseparator '{0}' is set wrongly: '{1}'".format(self._thousandSeparator, stringValue))

        try:
            self._checkThousandSeparator(thousandGroups[1:])
        except NumberFormatException as nfe:
            raise NumberFormatException(str(nfe) + " for value '{0}'.".format(stringValue))

    def _checkDecimalSeparator(self, stringValue, decimalGroups):
        if len(decimalGroups) > 1 and len(decimalGroups[1].split(self._thousandSeparator)) > 1:
            raise NumberFormatException("Decimalseparator '{0}' found in wrong position for value '{1}'.".format(self._decimalSeparator, stringValue))
        if len(decimalGroups) > 2:
            raise NumberFormatException("Decimalseparator '{0}' occurs more than once: '{1}'".format(self._decimalSeparator, stringValue))

    def _checkThousandSeparator(self, groups):
        for group in groups:
            if len(group) != 3:
                raise NumberFormatException("Thousandseparator '{0}' found in wrong position".format(self._thousandSeparator))
