#-------------------------------------------------------------------------
#
#  File Name   :  SMatrix
#
#  Description :
#
#   This module contains  the class 'SMatrix' which  implements a string
#   matrix (two-dimensional  array) for  easier access of  the elements,
#   but  not  with mathematical  calculations.   The  data structure  is
#   implemented as a row list of string lists.
#
#  Developer : Oskar Leirich                Creation date : 24.Jan.2023
#  Modified  : Oskar Leirich                Last changes  : 29.Jan.2023
#
#  This class contains following member functions :
#   of SMatrix :
#    of SMatrix:
#    SMatrix                   ~SMatrix                  addRow
#    copy                      deleteRow                 destroy
#    empty                     getCol                    getColText
#    getRow                    getRowText                getRowVec
#    getValue                  getValueText              operator ()
#    operator =                prependVec                reset
#    setRow                    setRowVec                 setValue
#    setValueText
#
#-------------------------------------------------------------------------

from __future__ import annotations

import re
from MatrixBase import MatrixBase
import StringUtils as strUtils

#-------------------------------------------------------------------------
#
#  Class Name   :  SMatrix.cpp
#
#  Description :
#
#   This class  implements a string  matrix (two-dimensional  array) for
#   easier   access  of   the  elements,   but  not   with  mathematical
#   calculations.  The data  structure is implemented as a  list of list
#   of strings.
#
#-------------------------------------------------------------------------

class SMatrix (MatrixBase) :

  #  The constructor initializes some variables.

  def __init__ ( self, rows : int = 0, cols : int = 0 ) :

    MatrixBase.__init__ ( self, rows, cols )

    self.nr : int      = 0
    self.nc : int      = 0
    self.nelems : int  = 0

    self.cleanQuotes   = True

    self.data = []
    self.matType = "String"


  #-------------------------------------------------------------------------
  #
  # Some getter and setter functions are defined here
  #
  #-------------------------------------------------------------------------

  def setCleanQuotes ( self, clean : bool ) :
    self.cleanQuotes = clean


  #-------------------------------------------------------------------------
  #
  #  Member function :  copy  of  SMatrix
  #
  #  Description :
  #
  #   This  function copies  the values  of  the given  SMatrix to  'this'
  #   matrix and returns a reference to 'this'.
  #
  #  Input parameters  :
  #    src             :  Reference to a SMatrix (const)
  #
  #-------------------------------------------------------------------------

  def copy ( self, src : SMatrix ) :

    self.data = src.data

    self.nr     = src.nr
    self.nc     = src.nc
    self.nelems = self.nr * self.nc


  #-------------------------------------------------------------------------
  #
  #  Member function :  addEmptyRow  of  SMatrix
  #
  #  Description :
  #
  #   This function adds an empty row to matrix.
  #
  #-------------------------------------------------------------------------

  def addEmptyRow (self) :

    dataRow : list

    dataRow = [""] * self.nc

    self.data.append (dataRow)

    self.nr = len ( self.data )


  #-------------------------------------------------------------------------
  #
  #  Member function :  addRow  of  SMatrix
  #
  #  Description :
  #
  #   This function adds the given row to the matrix.
  #
  #-------------------------------------------------------------------------

  def addRow ( self, row : SMatrix ) :

    if self.nr == 0 :
      self.nc = row.nCols ()

    self.addEmptyRow ()

    cols = min ( self.nc, row.nCols () )

    for col in range ( 0, cols ) :

      text = row.getValue ( 0, col )
      self.setValue ( self.nr - 1, col, text )


  #-------------------------------------------------------------------------
  #
  #  Member function :  addListRow  of  SMatrix
  #
  #  Description :
  #
  #   This function adds the given row to the matrix.
  #
  #-------------------------------------------------------------------------

  def addListRow ( self, strList : list ) :

    cols =len (strList)

    if self.nr == 0  :
      self.nc = cols

    self.addEmptyRow ()

    cols = min ( self.nc, cols )

    for col in range ( 0, cols ) :

      text = strList [col]
      self.setValue ( self.nr - 1, col, text )


  #-------------------------------------------------------------------------
  #
  #  Member function :  deleteRow  of  SMatrix
  #
  #  Description :
  #
  #   This  function removes  the row  with the  given index  in the  data
  #   vector.
  #
  #  Input parameters  :
  #   index            :  Index of the row to delete
  #
  #-------------------------------------------------------------------------

  def deleteRow ( self, index : int ) :

    del self.data [index]

    self.nr = len ( self.data )


  #-------------------------------------------------------------------------
  #
  #  Member function :  destroy  of  SMatrix
  #
  #  Description :
  #
  #   This function destroys the matrix by freeing all allocated memory.
  #
  #-------------------------------------------------------------------------

  def destroy (self) :

    self.nr : int      = 0
    self.nc : int      = 0
    self.nelems : int  = 0

    self.data = []


  #-------------------------------------------------------------------------
  #
  #  Member function :  empty  of  SMatrix
  #
  #  Description :
  #
  #   This function fills the matrix with empty strings.
  #
  #-------------------------------------------------------------------------

  def empty (self) :

    self.fill ( "" )


  #-------------------------------------------------------------------------
  #
  #  Member function :  fill  of  SMatrix
  #
  #  Description :
  #
  #   This function fills the matrix with the given string.
  #
  #-------------------------------------------------------------------------

  def fill ( self, value : str ) :

    if self.nr == 0 :
      return

    for i in range ( 0, self.nr ) :

      row : list = [value] * self.nc
      self.data [i] = row


  #-------------------------------------------------------------------------
  #
  #  Member function :  getDataTuples  of  SMatrix
  #
  #  Description :
  #
  #   This function returns the data matrix as a list of tuples.
  #
  #  Output parameters :
  #   (tuple)          : data matrix as a list of tuples.
  #
  #-------------------------------------------------------------------------

  def getDataTuples ( self ) -> list :

    data = []
    row  : tuple

    for idx in range ( 0, self.nr ) :

      row = tuple ( self.getRowList (idx) )
      data.append (row)

    return data


  #-------------------------------------------------------------------------
  #
  #  Member function :  getValue  of  SMatrix
  #
  #  Description :
  #
  #   This function returns the string value addressed by row and column.
  #
  #  Input parameters  :
  #    rown            :  row index    (starting with 0)
  #    coln            :  column index (starting with 0)
  #
  #  Output parameters :
  #    (str)           :  Value (string) at that point
  #
  #-------------------------------------------------------------------------

  def getValue ( self, rown : int, coln : int ) -> str :

    return self.data [rown] [coln]


  #-------------------------------------------------------------------------
  #
  #  Member function :  setValue  of  SMatrix
  #
  #  Description :
  #
  #   This function sets the string value addressed by row and column.
  #
  #  Input parameters  :
  #    rown            :  row index    (starting with 0)
  #    coln            :  column index (starting with 0)
  #    val             :  Value at that point
  #
  #-------------------------------------------------------------------------

  def setValue ( self, rown : int, coln : int, val : str ) :

    self.data [rown] [coln] = val


  #-------------------------------------------------------------------------
  #
  #  Member function :  getValueText  of  SMatrix
  #
  #  Description :
  #
  #   This function returns the addressed by row and column as text. It is
  #   overwritten by every derived classes to  allow a generic read of the
  #   matrix from file.
  #
  #  Input parameter  :
  #   rown            : row index (starting with 0)
  #   coln            : column index (starting with 0)
  #
  #  Output parameter :
  #   (string)        : Value addressed by  row and column
  #
  #-------------------------------------------------------------------------

  def getValueText ( self, rown : int, coln : int ) -> str :

    text = self.getValue ( rown, coln )

    return text



  #-------------------------------------------------------------------------
  #
  #  Member function :  setValueText  of  SMatrix
  #
  #  Description :
  #
  #   This function  sets the  value addressed  by row  and column.  It is
  #   overwritten  by derived  classes to  allow  a generic  write of  the
  #   matrix to file.
  #
  #  Input parameter  :
  #   rown            : row index (starting with 0)
  #   coln            : column index (starting with 0)
  #   value           : Value at that point
  #
  #-------------------------------------------------------------------------

  def setValueText ( self, rown : int, coln : int, value : str ) :

    if self.cleanQuotes :
      value = value.replace ( '"', "" )
      value = value.replace ( "\'", "" )

    self.setValue ( rown, coln, value )


  #-------------------------------------------------------------------------
  #
  #  Member function :  getCol  of  SMatrix
  #
  #  Description :
  #
  #   This  function returns  the column  with the  given index  in a  new
  #   string matrix as column vector with one column.
  #
  #  Input parameters  :
  #   index            :  Index of the wanted column
  #
  #  Output parameters :
  #   (SMatrix)        :  New matrix
  #
  #-------------------------------------------------------------------------

  def getCol ( self, index : int ) -> SMatrix :

    colMat = SMatrix ()

    colMat.reset ( self.nr, 1, "" )

    for row in range ( 0, self.nr ) :

      value = self.getValue ( row, index )
      colMat.setValue ( row, 0, value )

    colMat.setDelimiter (self.delimiter)

    return colMat


  #-------------------------------------------------------------------------
  #
  #  Member function :  getColList  of  SMatrix
  #
  #  Description :
  #
  #   This  function returns  the column  with the  given index  in a  new
  #   string list.
  #
  #  Input parameters  :
  #   index            :  Index of the wanted column
  #
  #  Output parameters :
  #   (QStringList)    :  Column values as string list
  #
  #-------------------------------------------------------------------------

  def getColList (  self, coln : int ) -> list :

    colText = []

    for i in range ( 0, self.nr ) :

      text = self.getValue ( i, coln )
      colText.append (text)

    return colText


  #-------------------------------------------------------------------------
  #
  #  Member function :  setColList  of  SMatrix
  #
  #  Description :
  #
  #   This function  sets the column  with the  given index to  the column
  #   vector.
  #
  #  Input parameters  :
  #   index            :  Index of the column vector (destination)
  #   col              :  String list as copy
  #
  #-------------------------------------------------------------------------

  def setColList ( self, col : list, index : int ) :

    if ( index >= self.nc ) :
      return

    for i in range ( 0, self.nr ) :
      text = str ( col [i] )
      self.setValue ( i, index, text )


  #-------------------------------------------------------------------------
  #
  #  Member function :  getColType  of  SMatrix
  #
  #  Description :
  #
  #   This function returns  the type of the column values  with the given
  #   index as  string. The type can  be integer, float, string  or string
  #   list of unique string values (categorical).
  #
  #  Input parameters  :
  #   index            :  Index of the wanted column
  #
  #  Output parameters :
  #   (QStringList)    :  Column values as string list
  #
  #-------------------------------------------------------------------------

  def getColType (  self, coln : int ) -> list :

    colTypes = []

    regex = re.compile ( "\d+:\d+" )

    for i in range ( 0, self.nr ) :

      text = self.getValue ( i, coln )

      while (1) :
        if strUtils.isInt (text) :
          if ( not "int" in colTypes ) :
            colTypes.append ( "int" )
          break

        if strUtils.isFloat (text) :
          if ( not "float" in colTypes ) :
            colTypes.append ( "float" )
          break

        if regex.search (text) :   # check for a time string
          text = "Time"

        if ( not text in colTypes ) :
          colTypes.append (text)

        break

    return colTypes


  #-------------------------------------------------------------------------
  #
  #  Member function :  getRow  of  SMatrix
  #
  #  Description :
  #
  #   This function returns  the row with the given index  in a new string
  #   matrix as row vector with one row.
  #
  #  Input parameters  :
  #   index            :  Index of the wanted row
  #
  #  Output parameters :
  #   (SMatrix)        :  New matrix
  #
  #-------------------------------------------------------------------------

  def getRow ( self, index : int ) -> SMatrix :

    rowMat = SMatrix ()

    rowMat.reset ( 1, self.nc, "" )

    for col in range ( 0, self.nc ) :

      value = self.getValue ( col, index )
      rowMat.setValue ( 0, col, value )

    rowMat.setDelimiter (self.delimiter)

    return rowMat


  #-------------------------------------------------------------------------
  #
  #  Member function :  getRowList  of  SMatrix
  #
  #  Description :
  #
  #   This function returns  the row with the given index  in a new string
  #   list.
  #
  #  Input parameters  :
  #   index            :  Index of the wanted row
  #
  #  Output parameters :
  #   (list)           :  String list as copy
  #
  #-------------------------------------------------------------------------

  def getRowList ( self, index : int ) -> list :

    row = []

    if index < len (self.data) :
      row = self.data [index]

    return row


  #-------------------------------------------------------------------------
  #
  #  Member function :  prependRow  of  SMatrix
  #
  #  Description :
  #
  #   This function at the given  string vector at the beginning (prepend)
  #   of the data vector.
  #
  #  Input parameters  :
  #   row              :  String vector to prepend
  #
  #-------------------------------------------------------------------------

  def prependRow ( self, row : list ) :

    self.data.insert ( 0, row )

    self.nr = len ( self.data )


  #-------------------------------------------------------------------------
  #
  #  Member function :  setRowList  of  SMatrix
  #
  #  Description :
  #
  #   This function sets the row with the given index in the data vector.
  #
  #  Input parameters  :
  #   index            :  Index of the row vector (destination)
  #   row              :  String list as copy
  #
  #-------------------------------------------------------------------------

  def setRowList ( self, row : list, index : int ) :

    if index < len (self.data) :
      self.data [index] = row


  #-------------------------------------------------------------------------
  #
  #  Member function :  setRow  of  SMatrix
  #
  #  Description :
  #
  #   This function adds the given row to the matrix.
  #
  #-------------------------------------------------------------------------

  def setRow ( self, src : SMatrix , srcIdx : int, dstIdx : int ) :

    if ( ( self.nc != src.nCols () ) or ( dstIdx >= self.nr ) or
         ( srcIdx >= src.nRows () ) ):
      return

    for col in range ( 0, self.nc ) :

      text = src.getValue ( srcIdx, col )
      self.setValue ( dstIdx, col, text )


  #-------------------------------------------------------------------------
  #
  #  Member function :  reset  of  SMatrix
  #
  #  Description :
  #
  #   This function resets the matrix  by allocating the needed memory and
  #   initializing the internal variables.
  #
  #  Input parameters  :
  #    rown            :  Number of rows
  #    coln            :  Number of columns
  #
  #-------------------------------------------------------------------------*/

  def reset ( self, rown : int, coln : int, value : str = "" ) :

    self.nr = rown
    self.nc = coln
    self.nelems  = rown * coln

    line : list

    self.data = []

    for i in range ( 0, rown ) :
      line = [value] * coln

      self.data.append (line)

