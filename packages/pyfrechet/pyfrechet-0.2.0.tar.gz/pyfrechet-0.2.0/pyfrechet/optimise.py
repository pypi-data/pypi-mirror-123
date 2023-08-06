## @package pyfrechet
#
#  Module for optimization algorithms; use to find minimum rechable epsilon.

import math
from decimal import Decimal

from .distance import Distance

## Binary search algorithm.
#
#  Use to find minimum epsilon for a path that exists in free space.
#  Can perform binary search on StrongDistance and WeakDistance
class BinarySearch:

    ## Private - left boundery of binary search.
    __l: float

    ## Private - right boundery of binary search.
    __r: float

    ## Private - middle value of binary search.
    __m: float

    ## Private - minimum percision of floating point.
    __p: float

    ## Constructs BinarySearch object.
    #  @param self Object pointer.
    #  @param StrongDistance or WeakDistance object.
    def __init__(self, distance):
        if isinstance(distance, Distance):
            self.__dis = distance
            self.__l = -1
            self.__r = -1
            self.__p = -8
        else:
            raise TypeError(f"{distance.__class__.__name__} is not a valid argument."
                            f"Must be of type StrongDistance or WeakDistance."
                            )

    @staticmethod
    def __vertexLength(c, n):
        l = 0
        for i in range(n-1):
            l += math.dist([c[i].x, c[i].y], [c[i+1].x, c[i+1].y])
        return l

    @staticmethod
    def __percision(p):
        return Decimal(str(p)).as_tuple().exponent

    ## Set inital boundeies for search().
    #  @param self Object pointer.
    #  @param left Inital left boundery.
    #  @param right Inital right boundery.
    def setBoundaries(self, left, right):
        self.__l = left
        self.__r = right

    ## Set inital boundeies for search.
    #  @param self Object pointer.
    #  @param percision Set minimum the floating point percision search() will return.
    def setPercision(self, precision):
        self.__p = self.__percision(precision)

    ## Recrusive method finds minimum epsilon for rechable path in freespace.
    #
    #  If setBoundaries() is not called, the inital bounderies are the
    #  maximum euclidean distance inside the freespace of the first and second
    #  curve. If setPercision() is not called, the default percision
    #  of the floating point returned is 1.0x10^-8.
    #  @param self Object pointer.
    #  @return Epsilon.
    def search(self):
        if self.__l == -1 and self.__r == -1:
            l1 = self.__vertexLength(self.__dis.getCurve2(), \
                self.__dis.getCurve2Lenght())
            l2 = self.__vertexLength(self.__dis.getCurve1(),\
                self.__dis.getCurve1Lenght())
            self.__l = 0
            self.__r = int(math.dist([l2, 0], [0, l1]))

        self.__m = (self.__l + self.__r) / 2
        self.__dis.setFreeSpace(self.__m)

        print(f"Checking if epsilon is reachable:")
        print(f"    | {self.__l} -- {self.__m} -- {self.__r} |")

        if self.__dis.isReachable():
            if self.__percision(self.__m) >= self.__p:
                print(f"    Eps {self.__m}: <reachable>\n")
                self.__r = self.__m
                return self.search()
            else:
                print(f"    Eps {self.__m}: <reachable> <meets percision>\n")
                return self.__m
        else:
            print(f"    Eps {self.__m}: <unreachable>\n")
            self.__l = self.__m
            return self.search()
