'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import TreatmentClass

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
        
    def testEqual(self):
        treatmentClass1 = TreatmentClass()
        self.assertNotEqual(treatmentClass1, None, "TreatmentClass should not be equal to None")
        self.assertNotEqual(treatmentClass1, "", "TreatmentClass should not be equal to str")
        
        treatmentClass2 = TreatmentClass()
        self.assertEqual(treatmentClass1, treatmentClass2, "Empty TreatmentClasses should not be equal")
        self.assertTrue(treatmentClass1 == treatmentClass2, "TreatmentClasses should be equal via '=='")
        self.assertFalse(treatmentClass1 != treatmentClass2, "TreatmentClasses should not be nonequal via '!='")
