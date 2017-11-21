'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from lxml import etree

from datamodel import Mime, Reference


class ReferenceTest(unittest.TestCase):

    def testInit(self):
        reference = Reference()

        self.assertIsNone(reference.referenceType)
        self.assertIsNone(reference.description)
        self.assertIsNone(reference.quantity)

        self.assertIsNone(reference.supplierArticleId)

        self.assertIsNotNone(reference.mimeInfo)
        self.assertEqual(len(reference.mimeInfo), 0)

    def testAddMime(self):
        reference = Reference()
        self.assertEqual(len(reference.mimeInfo), 0)
        reference.addMime(Mime())
        self.assertEqual(len(reference.mimeInfo), 0)
        mime = Mime()
        mime.mimeType = "image/jpg"
        mime.source = "image.jpg"
        mime.purpose = "normal"
        mime.order = 1
        reference.addMime(mime)
        self.assertEqual(len(reference.mimeInfo), 1)

    def testAddSupplierArticleId(self):
        reference = Reference()
        self.assertIsNone(reference.supplierArticleId)
        reference.addSupplierArticleId("test")
        self.assertEqual(reference.supplierArticleId, "test")

    # Testcases
    #
    #    if self.referenceType is None:
    #        super().logError("Der Referenz wurde kein Typ zugewiesen.",  raiseException)
    #    if self.supplierArticleIds is None or len(self.supplierArticleIds) == 0:
    #        super().logError("Es wird keine Artikelnummer referenziert.",  raiseException)
    def testValidateExceptionNoType(self):
        reference = Reference()
        with self.assertRaisesRegex(Exception, "Der Referenz wurde kein Typ zugewiesen."):
            reference.validate(True)

    def testValidateExceptionNoIds(self):
        reference = Reference()
        reference.referenceType = "sparepart"
        with self.assertRaisesRegex(Exception, "Es wird keine Artikelnummer referenziert."):
            reference.validate(True)

    def testValidate(self):
        reference = Reference()
        reference.referenceType = "sparepart"
        reference.addSupplierArticleId("Test")
        reference.validate(True)

    def testAddSecondId(self):
        reference = Reference()
        reference.referenceType = "sparepart"
        reference.addSupplierArticleId("Test")
        # zweites Mal hinzufügen, sollte einfach nur durchlaufen
        reference.addSupplierArticleId("Test")
        with self.assertRaisesRegex(Exception, "Es wird schon eine Artikelnummer referenziert: "):
            reference.addSupplierArticleId("Test2")

    def testEqual(self):
        reference1 = Reference()
        self.assertNotEqual(reference1, None, "Reference not equal to None")
        self.assertNotEqual(reference1, "", "Reference not equal to str")

        reference2 = Reference()

        self.assertEqual(reference1, reference2, "Empty References should be equal")
        self.assertTrue(reference1 == reference2, "Empty References should be equal via '==")
        self.assertFalse(reference1 != reference2, "Empty References should not be nonequal via '!='")

    def testValidateWithQuantity(self):
        reference = Reference()
        reference.referenceType = "sparepart"
        reference.addSupplierArticleId("Test")
        reference.quantity = 1
        reference.validate(True)

    def testValidateWithMime(self):
        reference = Reference()
        reference.referenceType = "sparepart"
        reference.addSupplierArticleId("Test")
        mime = Mime()
        mime.order = 1
        mime.source = "Test"
        mime.purpose = "detail"
        mime.mimeType = "image/jpeg"
        reference.addMime(mime)
        reference.validate(True)

    def testXmlConsistsOf(self):
        reference = Reference()
        reference.referenceType = "consists_of"
        reference.quantity = 1
        reference.addSupplierArticleId("Test")

        self.assertEqual(etree.tostring(reference.toXml()),
                         b'<ARTICLE_REFERENCE quantity="1" type="consists_of"><ART_ID_TO>Test</ART_ID_TO></ARTICLE_REFERENCE>',
                         "XML Ouput ist kaputt")


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
