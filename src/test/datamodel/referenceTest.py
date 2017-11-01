'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import Mime, Reference


class ReferenceTest(unittest.TestCase):

    def testInit(self):
        reference = Reference()
        
        self.assertIsNone(reference.referenceType)
        self.assertIsNone( reference.description)
        self.assertIsNone( reference.quantity)
        
        self.assertIsNone(reference.supplierArticleId)
        
        self.assertIsNotNone(reference.mimeInfo)
        self.assertEqual( len(reference.mimeInfo), 0)

    def testAddMime(self):
        reference = Reference()
        self.assertEqual( len(reference.mimeInfo), 0)
        reference.addMime(Mime())
        self.assertEqual( len(reference.mimeInfo), 1)    
            
    def testAddSupplierArticleId(self):
        reference = Reference()
        self.assertIsNone( reference.supplierArticleId)
        reference.addSupplierArticleId("test")
        self.assertEqual( reference.supplierArticleId, "test")
        
        
        
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
        
    def testEqual(self):
        reference1 = Reference()
        self.assertNotEqual(reference1, None, "Reference not equal to None")
        self.assertNotEqual(reference1, "", "Reference not equal to str")
        
        reference2 = Reference()
        
        self.assertEqual(reference1, reference2, "Empty References should be equal")
        self.assertTrue(reference1 == reference2, "Empty References should be equal via '==")
        self.assertFalse(reference1 != reference2, "Empty References should not be nonequal via '!='")
