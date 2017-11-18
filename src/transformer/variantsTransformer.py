'''
Created on 24.05.2017

@author: henrik.pilz
'''

class VariantsTransformer(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        
                            
    def createVariants(self, article):
        
        stepWidth = article.numberOfVariants
        numberOfIterations = 1
        
        
        for variantTuple in sorted(article.variants, key=lambda v: v[0]):
            variantFeatureName = variantTuple[1]
            variantValues = variantTuple[2].variants
            for i in range(1, numberOfIterations):
                for variantValue in variantValues:
                    for j in range(1,stepWidth):
                        pass
            numberOfIterations *= len(variantValues)