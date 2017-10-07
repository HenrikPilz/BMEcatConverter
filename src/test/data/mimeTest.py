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
        self.assertEqual( mime.order, 1 )

    def testValidateException(self):       
        with self.assertRaisesRegex(Exception, "Kein Bildpfad angegeben."):
            mime = Mime()
            mime.validate(True)
        
    def testValidate(self):
        mime = Mime()
        mime.source = "Test"
        mime.validate(True)
        mime.mimeType = "image/jpeg"
        mime.validate(True)
        mime.purpose = "detail"
        mime.validate(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    