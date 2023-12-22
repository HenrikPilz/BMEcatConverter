"""
Created on 22.12.2023

@author: henrik.pilz
"""

import unittest

from importer.xml import xmlUtils
from datamodel import ValidatingObject

class XMLUtilsImportTest(unittest.TestCase):

    def testNoValidatingObjectGivenNoneShouldReturnTrue(self):
        self.assertEqual(True, xmlUtils.noValidatingObject(None, "", False))

    def testNoValidatingObjectGivenObjectRaiseExceptionFalseShouldReturnFalse(self):
        validatingObject = ValidatingObject()
        self.assertEqual(False, xmlUtils.noValidatingObject(validatingObject, "", False))

    def testNoValidatingObjectGivenObjectRaiseExceptionTrueShouldRaiseException(self):
        with self.assertRaises(Exception):
            xmlUtils.noValidatingObject("validatingObject", "", True)

    def testObjectIsNoneGivenNoneShouldReturnTrue(self):
        self.assertEqual(True, xmlUtils.objectIsNone(None, "", False))

    def testObjectIsNoneGivenObjectRaiseExceptionFalseShouldReturnFalse(self):
        self.assertEqual(False, xmlUtils.objectIsNone("None", "", False))

    def testObjectIsNoneGivenObjectRaiseExceptionTrueShouldRaiseException(self):
        with self.assertRaises(Exception):
            xmlUtils.objectIsNone("None", "", True)

    def testObjectIsNotNoneGivenNoneShouldReturnFalse(self):
        self.assertEqual(False, xmlUtils.objectIsNotNone(None, "", False))

    def testObjectIsNotNoneGivenObjectRaiseExceptionFalseShouldReturnFalse(self):
        self.assertEqual(True, xmlUtils.objectIsNotNone("None", "", False))

    def testObjectIsNotNoneGivenObjectRaiseExceptionTrueShouldRaiseException(self):
        with self.assertRaises(Exception):
            xmlUtils.objectIsNotNone(None, "", True)

    def testObjectIsNotNoneAndNotEmptyGivenNoneShouldReturnFalse(self):
        self.assertEqual(False, xmlUtils.objectIsNotNoneAndNotEmpty(None, "", False))

    def testObjectIsNotNoneAndNotEmptyGivenEmptyArrayShouldReturnFalse(self):
        self.assertEqual(False, xmlUtils.objectIsNotNoneAndNotEmpty([], "", False))

    def testObjectIsNotNoneAndNotEmptyGivenEmptyStringShouldReturnFalse(self):
        self.assertEqual(False, xmlUtils.objectIsNotNoneAndNotEmpty("", "", False))

    def testObjectIsNotNoneAndNotEmptyGivenNonEmptyStringRaiseExceptionFalseShouldReturnTrue(self):
        self.assertEqual(True, xmlUtils.objectIsNotNoneAndNotEmpty("None", "", False))

    def testObjectIsNotNoneAndNotEmptyGivenNonEmptyArrayRaiseExceptionFalseShouldReturnTrue(self):
        self.assertEqual(True, xmlUtils.objectIsNotNoneAndNotEmpty(["None"], "", False))

    def testObjectIsNotNoneAndNotEmptyGivenNoneRaiseExceptionTrueShouldRaiseException(self):
        with self.assertRaises(Exception):
            xmlUtils.objectIsNotNoneAndNotEmpty(None, "", True)

    def testObjectIsNotNoneAndNotEmptyGivenEmptyStringRaiseExceptionTrueShouldRaiseException(self):
        with self.assertRaises(Exception):
            xmlUtils.objectIsNotNoneAndNotEmpty("", "", True)

    def testObjectIsNotNoneAndNotEmptyGivenEmptyArrayRaiseExceptionTrueShouldRaiseException(self):
        with self.assertRaises(Exception):
            xmlUtils.objectIsNotNoneAndNotEmpty([], "", True)

# if __name__ == '__main__':
#      unittest.main()
