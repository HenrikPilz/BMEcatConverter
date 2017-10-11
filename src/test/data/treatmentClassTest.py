'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data import TreatmentClass

class TreatmentClassTest(unittest.TestCase):

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
        
