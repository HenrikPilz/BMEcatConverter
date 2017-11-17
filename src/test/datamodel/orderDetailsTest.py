'''
Created on 16.07.2017

@author: Henrik Pilz
'''
import unittest

from datamodel import OrderDetails

class OrderDetailsTest( unittest.TestCase ):

    def testInit( self ):
        orderDetails = OrderDetails()

        self.assertEqual( orderDetails.orderUnit, "C62" )
        self.assertEqual( orderDetails.contentUnit, "C62" )
        self.assertEqual( orderDetails.packingQuantity, 1 )
        self.assertEqual( orderDetails.priceQuantity, 1 )
        self.assertEqual( orderDetails.quantityMin, 1 )
        self.assertEqual( orderDetails.quantityInterval, 1 )

    def testValidateExceptionNoOrderUnitSet( self ):
        orderDetails = OrderDetails()
        orderDetails.orderUnit = None
        with self.assertRaisesRegex( Exception, "Keine Bestelleinheit angeben." ):
            orderDetails.validate( True )
        orderDetails.orderUnit = ""
        with self.assertRaisesRegex( Exception, "Keine Bestelleinheit angeben." ):
            orderDetails.validate( True )

    def testValidateExceptionWrongOrderUnitSet( self ):
        orderDetails = OrderDetails()
        orderDetails.orderUnit = "Bla"
        with self.assertRaisesRegex( Exception, "Falsche Bestelleinheit angeben: " + str( orderDetails.orderUnit ) ):
            orderDetails.validate( True )

    def testValidateExceptionNoContentUnitSet( self ):
        orderDetails = OrderDetails()
        orderDetails.orderUnit = "C62"
        orderDetails.contentUnit = None
        with self.assertRaisesRegex( Exception, "Keine Verpackungseinheit angeben." ):
            orderDetails.validate( True )
        orderDetails.contentUnit = ""
        with self.assertRaisesRegex( Exception, "Keine Verpackungseinheit angeben." ):
            orderDetails.validate( True )

    def testValidateExceptionWrongContentUnitSet( self ):
        orderDetails = OrderDetails()
        orderDetails.orderUnit = "C62"
        orderDetails.contentUnit = "Blubb"
        with self.assertRaisesRegex( Exception, "Falsche Verpackungseinheit angeben: " + str( orderDetails.contentUnit ) ):
            orderDetails.validate( True )

    def testValidate( self ):
        orderDetails = OrderDetails()
        orderDetails.orderUnit = "C62"
        orderDetails.contentUnit = "C62"
        orderDetails.validate( True )
        orderDetails.quantityMin = 11
        orderDetails.validate( True )
        orderDetails.quantityInterval = 12
        orderDetails.validate( True )
        orderDetails.packingQuantity = 2
        orderDetails.validate( True )
        orderDetails.priceQuantity = 18
        orderDetails.validate( True )

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
