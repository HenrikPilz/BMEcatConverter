'''
Created on 04.01.2018

@author: henrik.pilz
'''


class ComparableEqual(object):
    '''
    Interface Class for a Class which are comparable
    '''

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def checkListForEquality(self, lhs, rhs):
        for leftItem in lhs:
            if leftItem not in rhs:
                return False

        for rightItem in rhs:
            if rightItem not in lhs:
                return False
        return True
