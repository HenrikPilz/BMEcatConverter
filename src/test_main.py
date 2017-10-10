import unittest
from test import data, exportHandler, xmlHandler

if __name__ == '__main__':
    # Datenmodultests
    unittest.main(data)
    # Mapper tests
    #unittest.main(test.mapping)
    # Resolver tests
    #unittest.main(test.resolver)
    # exportHandler tests
    unittest.main(exportHandler)
    # importHandler tests
    unittest.main(xmlHandler)
    # transformer tests
    #unittest.main(test.transformer)