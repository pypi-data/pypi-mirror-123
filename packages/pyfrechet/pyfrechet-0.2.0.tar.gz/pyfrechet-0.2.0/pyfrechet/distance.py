## @package pyfrechet
#
#  Module for working with Frechet distances.

from ._strong_distance import lib as _sd
from ._weak_distance import lib as _wd

import os

## Super class of StrongDistance and WeakDistance.
#
#  Class should not be used as a standalone object. Used in seperate modules
#  to check if StrongDistance and WeakDistance are instances of Distance
class Distance:

    ## Protected - filepath of file containing first curve.
    _curve_1_file: str

    ## Protected - filepath of file containing first curve.
    _curve_2_file: str

    ## Protected - last input of epsilon set to class.
    _epsilon: float

    ## Should be only called by sub classes.
    #  @param self Object pointer.
    #  @param curve_1_file Filepath of curve one.
    #  @param curve_2_file Filepath of curve one.
    def __init__(self, curve_1_file, curve_2_file):
        curve1_abspath = os.path.abspath(curve_1_file)
        curve2_abspath = os.path.abspath(curve_2_file)

        curve1_ascii = curve1_abspath.encode('ascii')
        curve2_ascii = curve2_abspath.encode('ascii')

        self._curve_1_file = curve1_ascii
        self._curve_2_file = curve2_ascii

    ## Formatted string containing curve filepaths and child class name.
    #  @param self Object pointer.
    #  @param name_ Name of sub class.
    #  @return Formatted string.
    def __str__(self, name_):
        try:
            curve_1_file, curve_2_file = self._curve_1_file, self._curve_2_file
        except:
            curve_1_file, curve_2_file = "N/A", "N/A"
        return f"""
                Frechet Distance       |  {name_}
                ========================================
                Curve 1 File           |  {curve_1_file}
                Curve 2 File           |  {curve_2_file}
                """

    ## Protected - raises IOError if sub class's setCurves() fails to read curve file.
    #  @param self Object pointer.
    #  @param errno Error number returned from C program.
    def _checkSetCurvesErrno(self, errno):
        if errno != 0:
            raise IOError(f"{os.strerror(errno)} raised while running setCurves().\n"
                          f"Check file paths and formats for error:\n"
                          f"{self._curve_1_file}\n"
                          f"{self._curve_2_file}"
                           )

    ## Use to get filepaths of curves.
    #  @param self Object pointer.
    #  @returns First curve filepath then second curve filepath.
    def getFileNames(self):
        return self._curve_1_file, self._curve_2_file

    ## Use to get last input of epsilon.
    #  @param self Object pointer.
    #  @returns Epsilon.
    def getEpsilon(self):
        return self._epsilon

## Frechet Distance API
#
#  Class can be used to load curves from files, build free space data structure
#  and check if paths exist in free space.
class StrongDistance(Distance):

    ## Constructs an empty object with no curves
    #  @param self Object pointer.
    def __init__(self):
        _sd.create_freespace_reachabilitytable()

    ## Formatted string containing curve filepaths and child class name.
    #  @param self Object pointer.
    #  @return Formatted string.
    def __str__(self):
        return super().__str__(self.__class__.__name__)

    ## Creates instance that includes two curves from two separate files.
    #  @param cls Class pointer.
    #  @param curve_1_file Filepath of file containing first curve.
    #  @param curve_2_file Filepath of file containing second curve.
    #  @param reverse_curve_2 True if coordinates for second curve need to be reversed.
    #  @return Object pointer.
    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, reverse_curve_2=False):
        self = cls.__new__(cls)
        super(StrongDistance, self).__init__(curve_1_file, curve_2_file)
        errno = _sd.createcurves(self._curve_1_file, self._curve_2_file, \
                                 reverse_curve_2)
        self._checkSetCurvesErrno(errno)
        self.__init__()
        return self

    ## Use to set free space data structure for epsilon.
    #  @param self Object pointer.
    #  @param epsilon Epsilon.
    def setFreeSpace(self, epsilon):
        self._epsilon = epsilon
        _sd.setfreespace(epsilon)

    ## Use to get coodinates of first curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve1(self):
        return _sd.getcurve1()

    ## Use to get coodinates of second curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve2(self):
        return _sd.getcurve2()

    ## Use to get number of coodinates for first curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve1().
    def getCurve1Lenght(self):
        return _sd.getcurve1lenght()

    ## Use to get number of coodinates for second curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve2().
    def getCurve2Lenght(self):
        return _sd.getcurve2lenght()

    ## Use to get free space data struct
    #  @param self Object pointer.
    #  @return Typedef struct freespace.
    def getFreeSpace(self):
        return _sd.getfreespace()

    ## Use to check if path exists inside free space.
    #  @param self Object pointer.
    #  @return True if path exists; False if path is not found.
    def isReachable(self):
        _sd.setreachabilitytable()
        return _sd.isreachable()

## Weak Frechet Distance API
#
#  Class can be used to load curves from files, build free space data structure
#  and check if paths exist in free space.
class WeakDistance(Distance):

    ## Constructs an empty object with no curves
    #  @param self Object pointer.
    def __init__(self):
        _wd.create_freespace_reachabilitytable()

    ## Formatted string containing curve filepaths and child class name.
    #  @param self Object pointer.
    #  @return Formatted string.
    def __str__(self):
        return super().__str__(self.__class__.__name__)

    ## Creates instance that includes two curves from two separate files.
    #  @param cls Class pointer.
    #  @param curve_1_file Filepath of file containing first curve.
    #  @param curve_2_file Filepath of file containing second curve.
    #  @param reverse_curve_2 True if coordinates for second curve need to be reversed.
    #  @return Object pointer.
    @classmethod
    def setCurves(cls, curve_1_file, curve_2_file, reverse_curve_2=False):
        self = cls.__new__(cls)
        super(WeakDistance, self).__init__(curve_1_file, curve_2_file)
        errno = _wd.createcurves(self._curve_1_file, self._curve_2_file, \
                                 reverse_curve_2)
        self._checkSetCurvesErrno(errno)
        self.__init__()
        return self

    ## Use to set free space data structure for epsilon.
    #  @param self Object pointer.
    #  @param epsilon Epsilon.
    def setFreeSpace(self, epsilon):
        self._epsilon = epsilon
        _wd.setfreespace(epsilon)

    ## Use to get coodinates of first curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve1(self):
        return _wd.getcurve1()

    ## Use to get coodinates of second curve
    #  @param self Object pointer.
    #  @return Array of coordinates; array of structs containing variables 'x' and 'y.'
    def getCurve2(self):
        return _wd.getcurve2()

    ## Use to get number of coodinates for first curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve1().
    def getCurve1Lenght(self):
        return _wd.getcurve1lenght()

    ## Use to get number of coodinates for second curve
    #  @param self Object pointer.
    #  @return Lenght of array returned by getCurve2().
    def getCurve2Lenght(self):
        return _wd.getcurve2lenght()

    ## Use to get free space data struct
    #  @param self Object pointer.
    #  @return Typedef struct freespace.
    def getFreeSpace(self):
        return _wd.getfreespace()

    ## Use to check if path exists inside free space.
    #  @param self Object pointer.
    #  @return True if path exists; False if path is not found.
    def isReachable(self):
        if _wd.getcurve1lenght() == 1 or _wd.getcurve2lenght() == 1:
            try:
                return _wd.computemaxdistances(super()._epsilon)
            except ValueError:
                raise ValueError("No value for Epsilon exists because"
                                 "setfreespace() was never called.")
        else:
            return _wd.isreachable()
