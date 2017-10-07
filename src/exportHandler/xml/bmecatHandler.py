'''
Created on 12.05.2017

@author: henrik.pilz
'''
from datetime import datetime
import csv
import logging
from xml.sax import handler
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from ElementTree_pretty import prettify
import datetime


from data import *

from xml.etree import ElementTree
from xml.dom import minidom



class BMEcatHandler(handler.ContentHandler):
    
    ''' alle registrierten StartElementhandler '''
    _startElementHandler = {
                "article" : "createProduct",
                "article_details" : "createProductDetails", 
                "order_details" : "createOrderDetails",
                "price_details" : "createPriceDetails",
                "price" : "createPrice",                
                "mime" : "createMime",
                "mime_info" : "startMimeInfo",
                "datetime" : "startDateTime",
                "article_features" :"createFeatureSet",
                "feature" : "createFeature",
                "special_treatment_class" : "createTreatmentClass",
                "article_reference" : "createReference" 
                }

    ''' Mögliche Aliase für Varianten der BMEcats '''
    _alias = {
                "product" : "article",
                "product_details" : "article_details",
                "supplier_pid" : "supplier_aid",
                "supplier_alt_pid" : "supplier_alt_aid",
                "manufacturer_pid" : "manufacturer_aid",
                "buyer_pid" : "buyer_aid",
                "article_order_details" : "order_details",
                "article_price_details" : "price_details",
                "article_price" : "price",
                "product_features" : "article_features",
                "international_pid" : "ean",
                "product_order_details" : "order_details",
                "product_price_details" : "price_details",
                "product_price" : "price",
                "product_reference" : "article_reference",
                "prod_id_to" : "art_id_to"
            }
            
    ''' alle registrierten EndElementhandler '''
    _endElementHandler = {
                "article_features" :"saveFeatureSet",
                "feature" : "saveFeature",
                "article" : "saveProduct",
                "mime_info" : "endMimeInfo",
                "datetime" : "endDateTime",
                "mime" : "saveMime",
                "supplier_aid" : "addArticleId",
                "supplier_alt_aid" : "addAlternativeArticleId",
                "buyer_aid" : "addAlternativeArticleId",
                "manufacturer_aid" : "addManufacturerArticleId",
                "manufacturer_name" : "addManufacturerName",
                "ean" : "addEAN", 
                "description_long" : "addDescription",
                "description_short" : "addTitle",
                "price" : "savePrice",
                "price_details" : "savePriceDetails",
                "delivery_time" : "addDeliveryTime",
                "price_amount" : "addPriceAmount",
                "tax" : "addPriceTax",
                "price_currency" : "addPriceCurrency",
                "price_factor" : "addPriceFactor",
                "territory" : "addTerritory",
                "lower_bound" : "addPriceLowerBound",
                "mime_source" : "addMimeSource",
                "mime_type" : "addMimeType",
                "mime_descr" : "addMimeDescription",
                "mime_alt" : "addMimeAlt",
                "mime_purpose" : "addMimePurpose",
                "mime_order" : "addMimeOrder",
                "order_unit" : "addOrderUnit",
                "content_unit" : "addContentUnit",
                "no_cu_per_ou " : "addPackagingQuantity",
                "price_quantity " : "addPriceQuantity",
                "quantity_min " : "addQuantityMin",
                "quantity_interval" : "addQuantityInterval",
                "date" : "addDate",
                "fname" : "addFeatureName",
                "fvalue" : "addFeatureValue",
                "fvalue_details" : "addFeatureValueDetails",
                "funit" : "addFeatureUnit",
                "fdesc" : "addFeatureDescription",
                "special_treatment_class" : "saveTreatmentClass",
                "catalog_group_system" : "resetAll",
                "article_reference" : "saveReference",
                "art_id_to" : "addReferenceArticleId",
                "reference_descr" : "addReferenceDescription"
                }

    def createHeader(self):
        ''' Create Header of BMEcat'''
        top = Element('top')

        comment = Comment('Generated for PyMOTW')
        top.append(comment)
        
        child = SubElement(top, 'child')
        child.text = 'This child contains text.'
        
        child_with_tail = SubElement(top, 'child_with_tail')
        child_with_tail.text = 'This child has regular text.'
        child_with_tail.tail = 'And "tail" text.'
        
        child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
        child_with_entity_ref.text = 'This & that'


        generated_on = str(datetime.datetime.now())
        
        # Configure one attribute with set()
        root = Element('opml')
        root.set('version', '1.0')
        
        root.append(Comment('Generated by ElementTree_csv_to_xml.py for PyMOTW'))
        
        head = SubElement(root, 'head')
        title = SubElement(head, 'title')
        title.text = 'My Podcasts'
        dc = SubElement(head, 'dateCreated')
        dc.text = generated_on
        dm = SubElement(head, 'dateModified')
        dm.text = generated_on
        
        body = SubElement(root, 'body')
        
        with open('podcasts.csv', 'rt') as f:
            current_group = None
            reader = csv.reader(f)
            for row in reader:
                group_name, podcast_name, xml_url, html_url = row
                if current_group is None or group_name != current_group.text:
                    # Start a new group
                    current_group = SubElement(body, 'outline', {'text':group_name})
                # Add this podcast to the group,
                # setting all of its attributes at
                # once.
                podcast = SubElement(current_group, 'outline',
                                     {'text':podcast_name,
                                      'xmlUrl':xml_url,
                                      'htmlUrl':html_url,
                                      })
                
        top = Element('top')

        children = [
            Element('child', num=str(i))
            for i in xrange(3)
            ]

top.extend(children)

print prettify(root)
        
        print self.prettify(top)

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    