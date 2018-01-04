'''
Module for the datastructures
'''

from datamodel.comparableEqual import ComparableEqual
from datamodel.feature import Feature
from datamodel.featureSet import FeatureSet
from datamodel.mime import Mime
from datamodel.orderDetails import OrderDetails
from datamodel.price import Price
from datamodel.priceDetails import PriceDetails
from datamodel.product import Product
from datamodel.productDetails import ProductDetails
from datamodel.reference import Reference
from datamodel.treatmentClass import TreatmentClass
from datamodel.validatingObject import FormulaFoundException
from datamodel.validatingObject import ValidatingObject
from datamodel.variant import Variant
from datamodel.variantSet import VariantSet
from datamodel.xmlObject import NoValueGivenException
from datamodel.xmlObject import ValidatingXMLObject
from datamodel.xmlObject import XMLObject

__all__ = ['Feature',
           'FeatureSet',
           'Mime',
           'Product',
           'ProductDetails',
           'OrderDetails',
           'PriceDetails',
           'Price',
           'Reference',
           'TreatmentClass',
           'Variant',
           'VariantSet']
