'''
Created on 09.01.2018

@author: henrik.pilz
'''
import unittest

from datamodel import XMLObject


class TestClass(XMLObject):
    def validate(self, raiseException=False):
        raise Exception("Nein")


class XMLObjectTest(unittest.TestCase):

    def testInit(self):
        XMLObject()

    def testValidateNotImplementedError(self):
        xmlObject = XMLObject()

        with self.assertRaisesRegex(NotImplementedError, "Please implement 'toXml' in your class '"):
            xmlObject.toXml()

    def testNoValueGivenException(self):
        xmlObject = XMLObject()

        with self.assertRaisesRegex(Exception, "'TestTag' Kein Wert übergeben."):
            xmlObject.addMandatorySubElement("testParent", "TestTag", None)

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
