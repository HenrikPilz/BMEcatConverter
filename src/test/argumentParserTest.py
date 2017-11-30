'''
Created on 19.11.2017

@author: Henrik Pilz
'''
from getopt import GetoptError
import unittest

from argumentParser import ArgumentParser
from argumentParser import HelpCalledException
from argumentParser import MissingArgumentException


class ArgumentParserTest(unittest.TestCase):

    def testParseArgumentsReturnHelpCalledException(self):
        argumentParser = ArgumentParser()
        with self.assertRaises(HelpCalledException):
            argumentParser.parse(['-h'])

    def testParseArgumentsReturnMissingArgumentException(self):
        argumentParser = ArgumentParser()
        argv = []
        with self.assertRaisesRegex(MissingArgumentException, "Inputfile is missing."):
            argumentParser.parse(argv)

        argv.append('-i')
        with self.assertRaisesRegex(GetoptError, "option -i requires argument"):
            argumentParser.parse(argv)

        argv.append('test.xml')
        with self.assertRaisesRegex(MissingArgumentException, "Outputfile is missing."):
            argumentParser.parse(argv)

        argv.append('-o')
        with self.assertRaisesRegex(GetoptError, "option -o requires argument"):
            argumentParser.parse(argv)

        # argv.append('test.xlsx')
        # with self.assertRaisesRegex(MissingArgumentException, "Dateformat is missing."):
        #    argumentParser.parse(argv)

        # argv.append('--dateformat="%Y-%m-%d"')
        # with self.assertRaisesRegex(MissingArgumentException, "SeparatorMode is missing."):
        #    argumentParser.parse(argv)

    def testParseArgumentsMinimalInput(self):
        argumentParser = ArgumentParser()
        argv = ['-i', 'test.xml', '-o', 'test.xlsx']
        argumentParser.parse(argv)
        self.assertEqual(argumentParser.inputfile, "test.xml", "Inputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.outputfile, "test.xlsx", "Outputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.dateformat, None, "Dateformat nicht richtig gesetzt.")
        self.assertEqual(argumentParser.separatorMode, None, "Separatormode nicht richtig gesetzt.")
        self.assertEqual(argumentParser.manufacturer, None, "Manufacturer nicht richtig gesetzt.")
        self.assertEqual(argumentParser.merchant, "fiege", "Merchant nicht richtig gesetzt.")

    def testParseArgumentsWithDateFormat(self):
        argumentParser = ArgumentParser()
        argv = ['-i', 'test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"']
        argumentParser.parse(argv)
        self.assertEqual(argumentParser.inputfile, "test.xml", "Inputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.outputfile, "test.xlsx", "Outputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.dateformat, '"%Y-%m-%d"', "Dateformat nicht richtig gesetzt.")
        self.assertEqual(argumentParser.separatorMode, None, "Separatormode nicht richtig gesetzt.")
        self.assertEqual(argumentParser.manufacturer, None, "Manufacturer nicht richtig gesetzt.")
        self.assertEqual(argumentParser.merchant, "fiege", "Merchant nicht richtig gesetzt.")

    def testParseArgumentsWithSeparators(self):
        argumentParser = ArgumentParser()
        argv = ['-i', 'test.xml', '-o', 'test.xlsx', '--separators="english"']
        argumentParser.parse(argv)
        self.assertEqual(argumentParser.inputfile, "test.xml", "Inputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.outputfile, "test.xlsx", "Outputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.dateformat, None, "Dateformat nicht richtig gesetzt.")
        self.assertEqual(argumentParser.separatorMode, '"english"', "Separatormode nicht richtig gesetzt.")
        self.assertEqual(argumentParser.manufacturer, None, "Manufacturer nicht richtig gesetzt.")
        self.assertEqual(argumentParser.merchant, "fiege", "Merchant nicht richtig gesetzt.")

    def testParseArgumentsWithMerchantSetToNone(self):
        argumentParser = ArgumentParser()
        argumentParser.merchant = None
        argv = ['-i', 'test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"', '--separators="english"']
        argv.append('--manufacturer=Test')
        argumentParser.parse(argv)
        self.assertEqual(argumentParser.inputfile, "test.xml", "Inputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.outputfile, "test.xlsx", "Outputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.dateformat, '"%Y-%m-%d"', "Dateformat nicht richtig gesetzt.")
        self.assertEqual(argumentParser.separatorMode, '"english"', "Separatormode nicht richtig gesetzt.")
        self.assertEqual(argumentParser.manufacturer, "Test", "Manufacturer nicht richtig gesetzt.")
        self.assertIsNone(argumentParser.merchant, "Merchant nicht richtig gesetzt.")

    def testParseArgumentsWithManufacturer(self):
        argumentParser = ArgumentParser()
        argv = ['-i', 'test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"', '--separators="english"']
        argv.append('--manufacturer=Test')
        argumentParser.parse(argv)
        self.assertEqual(argumentParser.inputfile, "test.xml", "Inputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.outputfile, "test.xlsx", "Outputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.dateformat, '"%Y-%m-%d"', "Dateformat nicht richtig gesetzt.")
        self.assertEqual(argumentParser.separatorMode, '"english"', "Separatormode nicht richtig gesetzt.")
        self.assertEqual(argumentParser.manufacturer, "Test", "Manufacturer nicht richtig gesetzt.")
        self.assertEqual(argumentParser.merchant, "fiege", "Merchant nicht richtig gesetzt.")

    def testParseArgumentsWithMerchant(self):
        argumentParser = ArgumentParser()
        argv = ['-i', 'test.xml', '-o', 'test.xlsx', '--dateformat="%Y-%m-%d"', '--separators="english"']
        argv.append('--merchant=Test')
        argumentParser.parse(argv)
        self.assertEqual(argumentParser.inputfile, "test.xml", "Inputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.outputfile, "test.xlsx", "Outputfile nicht richtig gesetzt.")
        self.assertEqual(argumentParser.dateformat, '"%Y-%m-%d"', "Dateformat nicht richtig gesetzt.")
        self.assertEqual(argumentParser.separatorMode, '"english"', "Separatormode nicht richtig gesetzt.")
        self.assertIsNone(argumentParser.manufacturer, "Manufacturer nicht richtig gesetzt.")
        self.assertEqual(argumentParser.merchant, "Test", "Merchant nicht richtig gesetzt.")


# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
