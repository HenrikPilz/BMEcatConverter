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
            mime.validate()
        except Exception as ve:
            assert ve == "Kein Bildpfad angegeben."

    def testValidate(self):
        mime = Mime()
        mime.source = "Test"
        mime.validate()
        mime.mimeType = "image/jpeg"
        mime.validate()
        mime.purpose = "detail"
        mime.validate()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    