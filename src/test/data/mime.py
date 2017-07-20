'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from data.mime import Mime

class TestMime(unittest.TestCase):

    def testInit(self):
        mime = Mime()
        assert mime.source == None
        assert mime.mimeType == None
        assert mime.description == None
        assert mime.altenativeContent == None
        assert mime.purpose == None
        assert mime.order == 1

    def testValidateException(self):
        mime = Mime()
        try:
            mime.validate(True)
            assert False
        except Exception as ve:
            assert str(ve) == "Kein Bildpfad angegeben."

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
    