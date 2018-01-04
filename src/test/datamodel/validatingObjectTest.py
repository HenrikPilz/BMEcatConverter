'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel.validatingObject import ValidatingObject


class TestClass(ValidatingObject):
    def validate(self, raiseException=False):
        raise Exception("Nein")


class ValidatingObjectTest(unittest.TestCase):

    def testInit(self):
        ValidatingObject()

    def testValidateNotImplementedError(self):
        validatingObject = ValidatingObject()

        with self.assertRaisesRegex(NotImplementedError, "Please implement 'validate' in your class '"):
            validatingObject.validate()

        with self.assertRaisesRegex(NotImplementedError, "Please implement 'validate' in your class '"):
            validatingObject.validate(True)

    def testAddException(self):
        validatingObject = ValidatingObject()

        with self.assertRaisesRegex(Exception, "Klassenattribut nicht gefunden: 'ValidatingObject' object has no attribute 'testList'"):
            validatingObject.add("testList", "Test")

    def testValidateListException(self):
        listToValidate = [TestClass()]

        with self.assertRaisesRegex(Exception, "Testoutput :: Nein"):
            ValidatingObject.validateList(listToValidate, "Testoutput", True)

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
