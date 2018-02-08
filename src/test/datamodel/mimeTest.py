'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import FormulaFoundException
from datamodel import Mime


class MimeTest(unittest.TestCase):

    def testInit(self):
        mime = Mime()
        self.assertIsNone(mime.source)
        self.assertIsNone(mime.mimeType)
        self.assertIsNone(mime.description)
        self.assertIsNone(mime.alternativeContent)
        self.assertIsNone(mime.purpose)
        self.assertIsNone(mime.order)

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
        with self.assertRaisesRegex(Exception, "Bildtyp fehlerhaft. Wert: test"):
            mime.validate(True)

    def testValidateExceptionNoPurpose(self):
        mime = Mime()
        mime.source = "Test.jpg"
        mime.order = 1
        mime.mimeType = "image/jpg"
        with self.assertRaisesRegex(Exception, "Bildverwendung nicht gesetzt."):
            mime.validate(True)

    def testValidateExceptionWrongPurpose(self):
        mime = Mime()
        mime.source = "Test.jpg"
        mime.order = 1
        mime.mimeType = "image/jpg"
        mime.purpose = "TEST"
        with self.assertRaisesRegex(Exception, "Bildverwendung fehlerhaft. Wert: TEST"):
            mime.validate(True)

    def testValidateExceptionFormulaFound(self):
        mime = Mime()
        mime.source = "=Test"
        mime.order = 1
        mime.mimeType = "image/jpg"
        mime.purpose = "detail"
        with self.assertRaisesRegex(FormulaFoundException, "Im Objekt vom Typ '.*' wurde im Feld .* ein Formeleintrag gefunden."):
            mime.validate(True)

    def testValidateExceptionFileTypeNotAllowed(self):
        mime = Mime()
        mime.source = "Test.eps"
        mime.order = 1
        mime.mimeType = "image/tif"
        mime.purpose = "detail"
        with self.assertRaisesRegex(Exception, "Bildpfad .* enthält eine nicht erlaubte Endung (.{3})."):
            mime.validate(True)

    def testValidate(self):
        mime = Mime()
        mime.order = 1
        mime.source = "Test.jpg"
        mime.purpose = "detail"
        mime.mimeType = "image/jpeg"
        mime.validate(True)

    def testValidateChangePath(self):
        mime = Mime()
        mime.order = 1
        mime.source = "/Dir1/Dir2/Filename.jpg"
        mime.purpose = "detail"
        mime.mimeType = "image/jpg"
        mime.validate(True)
        self.assertEqual(mime.source, "dir1/dir2/Filename.jpg", "Dateiname wurde nicht korrekt angepasst")

    def testValidateChangePathWithSpaces(self):
        mime = Mime()
        mime.order = 1
        mime.source = " /Dir1 /Dir2/File name.jpg"
        mime.purpose = "detail"
        mime.mimeType = "image/jpg"
        mime.validate(True)
        self.assertEqual(mime.source, "dir1/dir2/File_name.jpg", "Dateiname wurde nicht korrekt angepasst")

    def testValidateAdaptMimeType(self):
        mime = Mime()
        mime.order = 1
        mime.source = "/Dir1/Dir2/Filename.jpg"
        mime.purpose = "detail"
        mime.mimeType = "image/JPG"
        mime.validate(True)
        self.assertEqual(mime.mimeType, "image/jpg", "MimeType wurde nicht korrekt angepasst")

    def testEqual(self):
        mime1 = Mime()
        self.assertNotEqual(mime1, "", "Mime should not be equal to str")
        mime2 = Mime()
        self.assertEqual(mime1, mime2, "Empty mimes should be equal.")
        self.assertTrue(mime1 == mime2, "Empty mimes should be equal via '=='.")
        self.assertFalse(mime1 != mime2, "Empty mimes should not be unequal via '!='.")

        mime1.order = 1
        self.assertEqual(mime1, mime2, "Order should not matter")

        mime1.purpose = "detail"
        self.assertEqual(mime1, mime2, "Purpose should not matter")

        mime1.mimeType = "image/jpg"
        self.assertNotEqual(mime1, mime2, "Type should matter")
        mime2.mimeType = "image/jpg"
        self.assertEqual(mime1, mime2, "Same Type should work")

        mime1.source = "image.jpg"
        self.assertNotEqual(mime1, mime2, "Different source should matter")
        mime2.source = "image.jpg"
        self.assertEqual(mime1, mime2, "Same source should work")

        mime1.alternativeContent = "detail"
        self.assertEqual(mime1, mime2, "AltenativeContent should not matter")

        mime1.description = "detail"
        self.assertEqual(mime1, mime2, "Description should not matter")

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
