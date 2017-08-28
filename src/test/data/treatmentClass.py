'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.treatmentClass import TreatmentClass

class TestTreatmentClass(unittest.TestCase):

    def testInit(self):        
        treatmentClass = TreatmentClass()

        self.assertIsNone(treatmentClass.classType)
        self.assertIsNone(treatmentClass.value)

    def testValidateExceptionNoClassType(self):
        treatmentClass = TreatmentClass()
        with self.assertRaisesRegex(Exception, "Es muss eine Klassifizierung angegeben werden."):
            treatmentClass.validate(True)

    def testValidate(self):
        treatmentClass = TreatmentClass()
        treatmentClass.classType = "1"
        treatmentClass.validate(True)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    