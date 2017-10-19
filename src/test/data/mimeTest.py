'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data import Mime

class MimeTest(unittest.TestCase):

    def testInit(self):
        mime = Mime()
        self.assertIsNone( mime.source )
        self.assertIsNone( mime.mimeType )
        self.assertIsNone( mime.description )
        self.assertIsNone( mime.altenativeContent )
        self.assertIsNone( mime.purpose )
        self.assertIsNone( mime.order )

    def testValidateExceptionNoSource(self):       
        mime = Mime()
        with self.assertRaisesRegex(Exception, "Kein Bildpfad angegeben."):
            mime.validate(True)
        
    def testValidateExceptionNoOrder(self):
        mime = Mime()
        mime.source = "Test"
        with self.assertRaisesRegex(Exception, "Bildreihenfolge fehlerhaft: "):
            mime.validate(True)

    def testValidateExceptionNoMimeType(self):
        mime = Mime()
        mime.source = "Test"
        mime.order = 1
        with self.assertRaisesRegex(Exception, "Bildtyp nicht gesetzt."):
            mime.validate(True)
        
    def testValidateExceptionWrongMimeType(self):
        mime = Mime()
        mime.source = "Test"
        mime.order = 1
        mime.mimeType = "Test"
        with self.assertRaisesRegex(Exception, "Bildtyp fehlerhaft: Test"):
            mime.validate(True)
        
    def testValidateExceptionNoPurpose(self):
        mime = Mime()
        mime.source = "Test"
        mime.order = 1
        mime.mimeType = "image/jpg"
        with self.assertRaisesRegex(Exception, "Bildverwendung nicht gesetzt."):
            mime.validate(True)

    def testValidateExceptionWrongPurpose(self):
        mime = Mime()
        mime.source = "Test"
        mime.order = 1
        mime.mimeType = "image/jpg"
        mime.purpose = "TEST"
        with self.assertRaisesRegex(Exception, "Bildverwendung fehlerhaft: TEST"):
            mime.validate(True)


    def testValidate(self):
        mime = Mime()
        mime.order = 1
        mime.source = "Test"
        mime.purpose = "detail"
        mime.mimeType = "image/jpeg"
        mime.validate(True)

