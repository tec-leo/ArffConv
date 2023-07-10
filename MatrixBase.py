#-------------------------------------------------------------------------
#
#  File Name   :  MatrixBase
#
#  Description :
#
#   This module  contains the  base class  'MatrixBase' for  all derived
#   matrix classes  of different data  type, even strings  and variants.
#   The data structure is implemented as a row list of lists.
#
#
#  Developer : Oskar Leirich                Creation date : 24.Jan.2023
#  Modified  : Oskar Leirich                Last changes  : 29.Jan.2023
#
#
#  This class contains following member functions :
#   of MatrixBase :
#    of MatrixBase:
#    MatrixBase                ~MatrixBase               addRow
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

from FileUtils import FileUtils
import StringUtils as strUtils


#-------------------------------------------------------------------------
#
#  Class Name   :  MatrixBase
#
#  Description :
#
#   This  class is  the base  class for  all derived  matrix classes  of
#   different data types, like float, integer or strings.
#
#-------------------------------------------------------------------------

class MatrixBase :

  #  The constructor initializes some variables.

  def __init__ ( self, rows : int = 0, cols : int = 0 ) :

    self.data          = []
    self.colLabels     = []
    self.rowLabels     = []
    self.matType       = "Generic"
    self.title         = ""

    self.nr : int      = 0
    self.nc : int      = 0
    self.nelems : int  = 0
    self.checkDecPoint = False
    self.useDecPoint   = True
    self.withColLabels = False
    self.withRowLabels = False
    self.checkSparse   = False    # check for sparse matrix in read
    self.autoSeparator = False    # check automatically for delimiter

    self.decimalPoint  = "."
    self.delimiter     = "\t"

    if ( rows > 0 ) and ( cols > 0 ) :
      self.reset ( rows, cols )


  #  Default 'str' function used in print

  def __str__ (self) :

    return self.toText ()


  #-------------------------------------------------------------------------
  #
  # Some getter and setter functions are defined here
  #
  #-------------------------------------------------------------------------

  def nRows (self) -> int :
    return self.nr

  def nCols (self) -> int :
    return self.nc

  def length (self) -> int :
    return self.nelems

  def size (self) -> int :
    return self.nelems

  def useColLabels ( self, withLabels : bool ) :
    self.withColLabels = withLabels

  def useRowLabels ( self, withLabels : bool ) :
    self.withRowLabels = withLabels

  def useAutoSeparator ( self, autoSep : bool ) :
    self.autoSeparator = autoSep


  #-------------------------------------------------------------------------
  #
  #  Member function :  reset  of  MatrixBase
  #
  #  Description :
  #
  #   This function resets the matrix  by allocating the needed memory and
  #   initializing the internal variables. If this matrix contains already
  #   elements then 'destroy' is called first.
  #
  #  Input parameters  :
  #    rown            :  Number of rows
  #    coln            :  Number of columns
  #
  #-------------------------------------------------------------------------*/

  def reset ( self, rown : int, coln : int ) :

    self.nr = rown
    self.nc = coln
    self.nelems = rown * coln


  #-------------------------------------------------------------------------
  #
  #  Member function :  isEmpty  of  MatrixBase
  #
  #  Description :
  #
  #   This function checks  if the matrix is empty  and returns the result
  #   as boolean.
  #
  #  Output parameters :
  #   (bool)           :  True - matrix is empty
  #
  #-------------------------------------------------------------------------

  def isEmpty (self) -> bool :

    if ( self.nelems == 0 ) :
      return True
    else :
      return False

  #-------------------------------------------------------------------------
  #
  #  Member function :  checkDim  of  MatrixBase
  #
  #  Description :
  #
  #   This function  checks if the  given matrix has  identical dimensions
  #   and returns the result as boolean.
  #
  #  Output parameters :
  #   (bool)           :  True - both matrices have identical dimensions
  #
  #-------------------------------------------------------------------------*/

  def checkDim ( self, other ) -> bool :


    if ( self.nc == other.nCols () ) and ( self.nr == other.nRows () ) :
      return True

    return False


  #-------------------------------------------------------------------------
  #
  #  Member function :  getValueText  of  MatrixBase
  #
  #  Description :
  #
  #   This  function returns  the addressed  row  and column  as text.  It
  #   should be overwritten by derived classes  to allow a generic read of
  #   the matrix from file.
  #
  #  Input parameter  :
  #   rown            : row index (starting with 0)
  #   coln            : column index (starting with 0)
  #
  #  Output parameter :
  #   (string)        : Value addressed by  row and column
  #
  #-------------------------------------------------------------------------*/

  def getValueText ( self, rown : int, coln : int ) -> str :

    val = None

    if ( rown < self.nr ) and ( coln < self.nc ) :
      val = self.data [rown] [coln]

    return val


  #-------------------------------------------------------------------------
  #
  #  Member function :  setValueText  of  MatrixBase
  #
  #  Description :
  #
  #   This function sets the value addressed  by row and column. It should
  #   be overwritten  by derived classes to  allow a generic write  of the
  #   matrix to file.
  #
  #  Input parameter  :
  #   rown            : row index (starting with 0)
  #   coln            : column index (starting with 0)
  #   value           : Value at that point
  #
  #-------------------------------------------------------------------------*/

  def setValueText ( self, rown : int, coln : int, value ) :

    self.data [rown] [coln] = value


  #-------------------------------------------------------------------------
  #
  #  Member function :  getColLabels  of  MatrixBase
  #
  #  Description :
  #
  #   This function returns the 'labels' for the columns.
  #
  #-------------------------------------------------------------------------*/

  def getColLabels (self) -> list :

    return self.colLabels


  #-------------------------------------------------------------------------
  #
  #  Member function :  getRowLabels  of  MatrixBase
  #
  #  Description :
  #
  #   This function returns the 'labels' for the rows.
  #
  #-------------------------------------------------------------------------*/

  def getRowLabels (self) -> list :

    return self.rowLabels


  #-------------------------------------------------------------------------
  #
  #  Member function :  setColLabels  of  MatrixBase
  #
  #  Description :
  #
  #   This function sets the 'labels' for the columns.
  #
  #-------------------------------------------------------------------------*/

  def setColLabels ( self, labels : list ) :

    self.colLabels = labels


  #-------------------------------------------------------------------------
  #
  #  Member function :  setRowLabels  of  MatrixBase
  #
  #  Description :
  #
  #   This function sets the 'labels' for the rows.
  #
  #-------------------------------------------------------------------------*/

  def setRowLabels ( self, labels : list ) :

    self.rowLabels = labels


  #-------------------------------------------------------------------------
  #
  #  Member function :  setDecimalPoint  of  MatrixBase
  #
  #  Description :
  #
  #   This  function sets  the  'decimal points'  character  to the  given
  #   value.  The  chosen  character is used  to replace if in  the values
  #   converting to text and writing to a file.
  #
  #  Input parameter  :
  #   decPoint        :  New value for the decimalPoint
  #
  #-------------------------------------------------------------------------*/

  def setDecimalPoint ( self, decPoint : str ) :

    self.decimalPoint = decPoint
    self.useDecPoint  = True


  #-------------------------------------------------------------------------
  #
  #  Member function :  setDelimiter  of  MatrixBase
  #
  #  Description :
  #
  #   This function  sets the  'separator' character  to the  given value.
  #   The chosen field separator is used when writing to a file.
  #
  #  Input parameter  :
  #   delimiter       :  New value for the field separator
  #
  #-------------------------------------------------------------------------*/

  def setDelimiter ( self, delimiter : str ) :

    self.delimiter = delimiter


  #-------------------------------------------------------------------------
  #
  #  Member function : fromText  of  MatrixBase
  #
  #  Description :
  #
  #   This  function writes  the  values  from the  string  list with  tab
  #   separated values into the matrix.
  #
  #-------------------------------------------------------------------------*/

  def fromText ( self, lines : list ) -> bool :

    parts : list
    line  : str
    value : str
    ok    : bool

    ok = True

    if self.autoSeparator :
      rowIdx = min ( 5, len (lines) )
      tmpList = lines [ 0 : rowIdx ]  # 5 lines should be enough
      self.delimiter = strUtils.getDelimiter (tmpList)

    if self.withColLabels :
      line = lines [0]
      del lines [0]

      self.colLabels = line.split (self.delimiter)

    rows = len (lines)

    if ( self.nr != rows ) :

      ok = False

      self.reset ( rows, self.nc )

    self.rowLabels = []

    for row in range ( 0, self.nr ) :
      line  = lines [row]
      parts = line.split (self.delimiter)

      cols = len (parts)

      if self.withRowLabels :
        cols = cols - 1

        self.rowLabels [row] = parts [0]  # contains label
        del parts [0]                     # remove label

      if ( self.nc != cols ) :
        if ( row == 0 )  :  # first row, allow a resize

          self.reset ( self.nr, cols )
        else :
          cols = min ( cols, self.nc )
          ok   = False

      for col in range ( 0, cols ) :
        value = parts [col]
        self.setValueText ( row, col, value )

    return ok


  #-------------------------------------------------------------------------
  #
  #  Member function : toText  of  MatrixBase
  #
  #  Description :
  #
  #  This function writes the matrix in  a tabular form and returns it in
  #  a string list.
  #
  #-------------------------------------------------------------------------*/

  def toText (self) -> list :

    lines : list
    parts : list
    line  : str
    tmp   : str

    lines = []   # delete lines

    if self.withColLabels :
      line = self.delimiter.join (self.colLabels)
      lines.append (line)

    for row in range ( 0, self.nr ) :

      parts = []     # delete temp list

      if self.withRowLabels :
        parts.append ( self.rowLabels [row] )

      for col in range ( 0, self.nc ) :

        tmp = self.getValueText ( row, col )

        if self.checkDecPoint :
          if self.useDecPoint :
            if ( self.decimalPoint == ',' ) :
              tmp = tmp.replace ( ".", "," )
            else :
              tmp = tmp.replace ( ",", "." )

        parts.append (tmp)

      line = self.delimiter.join (parts)

      lines.append (line)

    return lines


  #-------------------------------------------------------------------------
  #
  #  Member function : read  of  MatrixBase
  #
  #  Description :
  #
  #   This function reads the matrix in a tabular form from the given text
  #   file.
  #
  #  Input parameters   :
  #   fileName          :  Name of the text file
  #
  #-------------------------------------------------------------------------*/

  def read ( self, fileName : str ) -> bool :

    lines : list
    parts : list
    line  : str
    msg   : str

    fileUtils = FileUtils ()

    fileUtils.setFileName (fileName)

    ok, lines = fileUtils.readFile ()

    if not ok () :
      msg = "Matrix read : cannot read from file " + fileName
      print (msg)

      return False

    if ( len (lines) < 1 ) :

      msg = "Matrix read : File " + fileName + " is empty !"
      print (msg)

      return False

    line = lines [0]
    del lines [0]

    # split at white spaces
    parts = line.split ( "\t" )

    line = parts [0]

    if ( len (parts) < 3 ) or ( line.find ( "-Matrix:" ) < 0 )  :

      msg = "Matrix read : " + fileName + " is not a matrix file!"
      print (msg)

      return False

    rows = int ( parts [1] )
    cols = int ( parts [2] )

    self.reset ( rows, cols )

    return self.fromText (lines)


  #-------------------------------------------------------------------------
  #
  #  Member function : write  of  MatrixBase
  #
  #  Description :
  #
  #   This function writes the matrix in  a tabular form to the given text
  #   file.
  #
  #  Input parameters   :
  #   fileName          :  Name of the text file
  #   title             :  Title of the matrix
  #
  #-------------------------------------------------------------------------*/

  def write ( self, fileName : str, append : bool = False ) -> bool :

    lines : list

    text = "-Matrix:\t{0} rows\t{1} columns".format ( self.nr, self.nc )

    if self.title :
      text = text + "\t" + self.title

    text = self.matType + text

    lines = self.toText ()

    lines.insert ( 0, text )

    fileUtils = FileUtils ()

    fileUtils.setFileName (fileName)

    ok = fileUtils.writeFile ( lines, append )

    return ok
