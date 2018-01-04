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
        return self.__everyElementOfLeftListIsInRightList(lhs, rhs) and self.__everyElementOfLeftListIsInRightList(rhs, lhs)

    @classmethod
    def __everyElementOfLeftListIsInRightList(self, leftList, rightList):
        for leftListItem in leftList:
            if leftListItem not in rightList:
                return False
        return True
