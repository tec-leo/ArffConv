# -------------------------------------------------------------------------
#
#  Class       :  ArffConv
#
#  Description :
#
#   ARFF ( Attribute-Relation File Format ) is a file format for datasets
#   which are commonly used for machine
#   learning experiments.  This  file format was created to
#   be  used in  Weka, a  framework for machine  learning
#   automated experiments.
#
#   This module contains the class 'ArffConv' which implements functions
#   to read and write ARFF files in Python.
#
#   ARFF ( Attribute-Relation  File Format ) is a  file format specially
#   created for  describe datasets which  are commonly used  for machine
#   learning experiments and software.  This  file format was created to
#   be  used in  Weka, a  representative software  for machine  learning
#   automated experiments.
#
#   An ARFF file can be divided  into two sections: header and data. The
#   Header describes  the metadata of  the dataset, including  a general
#   description of the dataset, its name and its attributes.
#
#
#  Developer : Oskar Leirich                Creation date : 16.Jan.2023
#  Modified  : Oskar Leirich                Last changes  : 02.Mar.2023
#
#
#   This unit contains following member functions :
#    of ArffConv
#     ArffConv                  convData                  load
#     readField                 readFile                  save
#     setFile                   writeField                writeHeader
#
# -------------------------------------------------------------------------

import os
import re
import pandas as pd

# sys.path.append ( '../../Utils' )

from FileUtils import FileUtils
import StringUtils as strUtils
from SMatrix import SMatrix


#-------------------------------------------------------------------------
#
#  Class Name   :  ArffConv.cpp
#
#  Description :
#
#   This  class contains  functions  to  read and  write  ARFF files  in
#   Python.
#
#-------------------------------------------------------------------------

class ArffConv :

  #  The constructor initializes various member variables

  def __init__ (self) :

    self.attributes  = []       # list of attribute maps
    self.attrNames   = []       # list of attribute names
    self.relation    = ""       # description of the arff file
    self.dataFrame   = None     # data as pandas dataframe
    self.dataList    = []       # data of the arff file (float64 or string)
    self.dataType    = []       # list of maps with information (datatype)
    self.header      = []       # header of the arff file (string list)
    self.isValid     = False    # data and header format is correct or not
    self.attrChanged = False    # an attribute was explicitly changed
    self.fileName    = ""
    self.delimiter   = ","

    self.fileUtils   = FileUtils ()
    self.strMatrix   = SMatrix ()


  # The destructor does nothing for now

  def __del__ (self) :

    self.fileName = ""
    self.fileUtils.closeFile ()   # close any open file



  #-------------------------------------------------------------------------
  #
  #  Member function :  init  of  ArffConv
  #
  #  Description :
  #
  #   This function initializes some member variables.
  #
  #-------------------------------------------------------------------------

  def init (self) :

    self.attributes  = []       # list of attribute maps
    self.attrNames   = []       # list of attribute names
    self.relation    = ""       # description of the arff file
    self.dataFrame   = None     # data as pandas dataframe
    self.dataList    = []       # data of the arff file (float64 or string)
    self.dataType    = []       # list of maps with information (datatype)
    self.header      = []       # header of the arff file (string list)
    self.isValid     = False    # data and header format is correct or not
    self.attrChanged = False    # an attribute was explicitly changed
    self.fileName    = ""
    self.delimiter   = ","


  #-------------------------------------------------------------------------
  #
  #  Member function :  convData  of  ArffConv
  #
  #  Description :
  #
  #   This function converts the header and  data lists into a pandas data
  #   frame.  This  is done by preparing  a csv file with  attribute names
  #   and data let pandas read it.
  #
  #-------------------------------------------------------------------------

  def convData (self) :

    tmpName = "tmp_" + os.path.basename (self.fileName) + ".dat"
    self.fileUtils.setFileName (tmpName)

    header = self.delimiter.join ( self.attrNames )

    data : list = self.dataList
    data.insert ( 0, header )

    ok = self.fileUtils.writeFile (data)

    if not ok :
      return ok

    # restore original filename
    self.fileUtils.setFileName (self.fileName)

    self.dataFrame = pd.read_csv ( tmpName, sep = self.delimiter )

    os.remove (tmpName)

    return ok


  #-------------------------------------------------------------------------
  #
  #  Member function :  buildData  of  ArffConv
  #
  #  Description :
  #
  #   This function converts the header and  data lists into a pandas data
  #   frame.  This  is done by preparing  a csv file with  attribute names
  #   and data let pandas read it.
  #
  #-------------------------------------------------------------------------

  def buildData (self) -> bool :

    if ( not self.dataList ) or ( not self.attrNames ) :
      return False

    changed = self.parseData ( self.dataList )

    if changed :
      self.dataList = self.strMatrix.toText ()

    self.delimiter = ","    # make sure it is Arff delimiter

    values = self.strMatrix.getDataTuples ()

    self.dataFrame = pd.DataFrame ( values, columns = self.attrNames )

    self.convArffTypes ()    # data frame must already exist

    self.attrChanged = False

    return True


  #-------------------------------------------------------------------------
  #
  #  Member function :  convArffType  of  ArffConv
  #
  #  Description :
  #
  #   This function evaluates the arff datatype with the given indexes and
  #   sets the corresponding dataframe  type.  The keywords numeric, real,
  #   integer, string and date are case-insensitive.
  #
  #   The date attribute has a special format specifier
  #   @attribute <name> date [<date-format>]
  #
  #   The default  format string  accepts the  ISO-8601 combined  date and
  #   time format "yyyy-MM-dd'T'HH:mm:ss".  Dates must be specified in the
  #   data  section as  the  corresponding string  representations of  the
  #   date/time. A simple date format is e.g. "yyyy-MM-dd"
  #
  #
  #   Example :
  #    date     --> datetime64
  #    REAL     --> float64
  #    NUMERIC  --> int64
  #    yes,no   --> object
  #
  #-------------------------------------------------------------------------

  def convArffType ( self, index ) :

    # info is a reference, copy back not necessary
    info = self.attributes [index]

    arffType = info ["arffType"].lower ()
    attrName = info ["name"]

    dataType = "object"   # default

    while (1) :       # simulate switch case with strings
      if arffType == "real" :
        dataType = "float64"
        break

      if ( arffType == "integer" ) or ( arffType == "numeric" ) :
        dataType = "int64"
        break

      if arffType.startswith ("date") :
        dataType = "datetime64"

        arffType = info ["arffType"]  # exact case needed, no lower ()
        date = arffType [4:]
        info ["arffType"] = "date"

        info ["ARFF dateformat"] = date

        date, onlyTime = self.convDateFormat (date)

        info ["df dateformat"] = date

        df = self.dataFrame    #  just a reference

        try :     # to_timedelta is not working, only to_datetime
          df [attrName] = pd.to_datetime ( df [attrName], format=date )
        except :
          msg = "Cannot convert datatime format : " + arffType [4:]
          print (msg)

      break   # exit while if nothing is found, unconditional break

    info ["dataType"] = dataType    # type in data frame

    if ( dataType != "datetime64" ) :
      self.dataFrame [attrName] = self.dataFrame [attrName].astype (dataType)

    return dataType


  #-------------------------------------------------------------------------
  #
  #  Member function :  convArffTypes  of  ArffConv
  #
  #  Description :
  #
  #   This   function  evaluates   the   arff  datatypes   and  sets   the
  #   corresponding dataframe type.  The  keywords numeric, real, integer,
  #   string and date are case-insensitive.
  #
  #-------------------------------------------------------------------------

  def convArffTypes (self) :

    dfTypes = []

    for index in range ( 0, len (self.attributes) ) :

      dataType = self.convArffType (index)

      dfTypes.append (dataType)

    return dfTypes


  #-------------------------------------------------------------------------
  #
  #  Member function :  convDataType  of  ArffConv
  #
  #  Description :
  #
  #   This   function  evaluates   the  dataframe   types  and   sets  the
  #   corresponding arff datatype.
  #
  #   Example :
  #    float64    --> real
  #    int64      --> integer
  #    object     --> object    note format must be evaluated
  #    datetime64 --> date      note format must be evaluated
  #
  #-------------------------------------------------------------------------

  def convDataType (self) :

    dtypes = self.dataFrame.dtypes

    arffType : str

    for idx in range ( 0, len (dtypes) ) :

      datatype = dtypes [idx]
      dfname   = datatype.name

      arffType = "string"   # default

      info = {}

      while (1) :       # simulate switch case with strings
        if dfname.startswith ("float64") :
          arffType = "real"
          break

        if dfname.startswith ("int" ) :
          arffType = "integer"
          break

        if dfname.startswith ("datetime" ) :
          arffType = "date"
          info ["ARFF dateformat"] = "dd-MM-yyyy HH:mm:ss"
          break

        if dfname.startswith ("object") :
          colTypes = self.strMatrix.getColType (idx)

          if ( len (colTypes) > 1 ) :     # string is default
            arffType = ",".join (colTypes)
            arffType = "{" + arffType + "}"
          else :
            arffType = colTypes  [0]
          break

        break   # exit while if nothing is found, unconditional break

      info ["name"] = self.attrNames [idx]
      info ["arffType"] = arffType
      info ["dataType"] = dfname

      self.attributes.append (info)


  #-------------------------------------------------------------------------
  #
  #  Member function :  convDateFormat  of  ArffConv
  #
  #  Description :
  #
  #   This function converts the arff date / time format to a format for a
  #   pandas dataframe. This means any delimiters like ':', '-' or '/' are
  #   converted to '%'.
  #
  #-------------------------------------------------------------------------

  def convDateFormat ( self, arffDate ) -> tuple :

    dateStr = arffDate.strip ()
    dateStr = dateStr.replace ( '"', "" )
    dateStr = dateStr.replace ( "\'", "" )

    # convert time dateStr from Java's SimpleDateFormat to C's format
    dateFormat = None
    onlyTime   = True

    if "yyyy" in dateStr :
      dateStr = dateStr.replace ( "yyyy", "%Y" )
      dateFormat = "Y"
      onlyTime   = False
    elif "yy" in dateStr :
      dateStr = dateStr.replace ( "yy", "%y" )
      dateFormat = "Y"
      onlyTime   = False

    if "MM" in dateStr :
      dateStr = dateStr.replace ( "MM", "%m" )
      dateFormat = "M"
      onlyTime   = False

    if "dd" in dateStr :
      dateStr = dateStr.replace ( "dd", "%d" )
      dateFormat = "D"
      onlyTime   = False

    if "HH" in dateStr :
      dateStr = dateStr.replace ( "HH", "%H" )
      dateFormat = "h"

    if "mm" in dateStr :
      dateStr = dateStr.replace ( "mm", "%M" )
      dateFormat = "m"

    if "ss" in dateStr :
      dateStr = dateStr.replace ( "ss", "%S" )
      dateFormat = "s"

    if "z" in dateStr or "Z" in dateStr :
        raise ValueError ( "Date type attributes with time zone not "
                           "supported, yet" )

    if dateFormat is None:
      raise ValueError ( "Invalid or unsupported date format" )

    return dateStr, onlyTime


  #-------------------------------------------------------------------------
  #
  #  Member function :  evalDelimiter  of  ArffConv
  #
  #  Description :
  #
  #   This function evaluates the delimiter from the list and returns
  #   it as string.
  #
  #   Example for a list:
  #    sunny,80.0,90.0,TRUE,no
  #    overcast,83.0,86.0,FALSE,yes
  #    rainy,70.0,96.0,FALSE,yes
  #
  #   with quotes:
  #     @ATTRIBUTE timestamp DATE "yyyy-MM-dd HH:mm:ss"
  #
  #     @DATA
  #     "2001-04-03 12:12:12"
  #     "2001-05-03 12:59:55"
  #
  #-------------------------------------------------------------------------

  def evalDelimiter (self) :

    tmpList = self.dataList [ 0 : 5 ]  # 5 lines should be enough

    # check for quotes attributes
    for row in range ( 0, len (tmpList) ) :
      line  = tmpList [row]

      index = line.find ( '"' )

      # use non-greedy quantifier ".+?" to replace all individual occurrences
      if index >= 0 :
        line = re.sub ( r'".+?"', "column - " + str (row), line )
        tmpList [row] = line

      index = line.find ( "\'" )

      # non-greedy, do not match the content between first and last occurrences
      if index >= 0 :
        line = re.sub ( r'\'.+?\'', "column - " + str (row), line )
        tmpList [row] = line

    self.delimiter = strUtils.getDelimiter (tmpList)


  #-------------------------------------------------------------------------
  #
  #  Member function : parseData  of  ArffConv
  #
  #  Description :
  #
  #   This  function writes  the values  from the  string list  with comma
  #   separated values into the matrix. This specific version also handles
  #   sparse matrix and an optional weight  at the end.  Sparse matrix and
  #   weights are surrounded by curly braces.
  #
  #   Example for a sparse matrix :
  #
  #   @data
  #   {1 X, 3 Y, 4 "class A"}
  #   {2 W, 4 "class B"}
  #
  #   A weight can be associated with  an instance in a standard ARFF file
  #   by  appending it  to  the end  of  the line  for  that instance  and
  #   enclosing the value in urly braces.
  #
  #   Example for a weight at the end:
  #
  #   @data
  #   0, X, 0, Y, "class A", {5}
  #
  #   For a sparse instance, this example would look like:
  #
  #   @data
  #   {1 X, 3 Y, 4 "class A"}, {5}
  #
  #   Note that any instance without a weight value specified is assumed to
  #   have a weight of 1 for backwards compatibility.
  #
  #-------------------------------------------------------------------------*/

  def parseData ( self, lines : list ) -> bool :

    parts  : list
    line   : str
    value  : str
    weight : bool

    weight = False
    sparse = False

    rows   = len (lines)
    cols   = len ( self.attrNames )

    if cols == 1 :
      self.delimiter = "only one column"

    self.strMatrix.setDelimiter (self.delimiter)

    # compile regex for an optional weight at the end of a line
    regex = re.compile ( ",\s*{.+?}$" )

    # first check for sparse matrix and weight
    for row in range ( 0, rows ) :
      line  = lines [row]

      result = regex.search (line)   # check for a weight at the line end

      if result :
        weight = True
        break

    if weight :
      cols = cols + 1           # additional column for the weight

      self.attrNames.append ( "weight" )
      info : dict = { "name" : "weight", "arffType" : "real" }
      self.attributes.append (info)

    sMat = self.strMatrix       # reference to strMatrix

    sMat.reset ( rows, cols )   # new size (shape or dimension)
    sMat.fill ( "0" )   # new size (shape or dimension)

    if weight :
      parts = [ "1.0" ] * rows    # defaults
      sMat.setColList ( parts, cols - 1 )

    for row in range ( 0, rows ) :
      line  = lines [row]

      if weight :
        result = regex.search (line)   # check for a weight at the line end

        if result :     # weight found, check for floating point value ?
          # split manually preserve optional "{" of a sparse matrix
          idx1, idx2 = result.span ()

          value = line [ idx1 + 1 : -1 ]
          value = value.strip ()
          value = value.replace ( "{", "" )
          line  = line [ 0:idx1 ]

          sMat.setValueText ( row, cols - 1, value.strip () )

      if not line.startswith ( "{" ) :   # no sparse matrix
        parts = line.split ( "," )

        for col in range ( 0, len (parts) ) :
          value = parts [col]
          sMat.setValueText ( row, col, value )

        continue

      # sparse matrix in this line
      line = line.replace ( "{", "" )
      line = line.replace ( "}", "" )

      sparse = True

      rowLine : list = line.split ( "," )

      for col in range ( 0, len (rowLine) ) :
        entry = rowLine [col]
        key : list = entry.split ( " " )
        index = int ( key [0] )
        value = key [1]

        sMat.setValueText ( row, index, value )

    changed = sparse or weight

    return changed


  #-------------------------------------------------------------------------
  #
  #  Member function :  parseHeader  of  ArffConv
  #
  #  Description :
  #
  #   This function parses  the header for attributes  and the description
  #   (relation).
  #
  #   Example
  #
  #    @RELATION weather
  #
  #    @ATTRIBUTE outlook {sunny, overcast, rainy}
  #    @ATTRIBUTE temperature REAL
  #    @ATTRIBUTE humidity REAL
  #    @ATTRIBUTE windy {TRUE, FALSE}
  #    @ATTRIBUTE play {yes, no}
  #
  #    if the attribute name contains spaces, it must be quoted with
  #    single or double quotes:
  #    @ATTRIBUTE "previous humidity" REAL
  #
  #-------------------------------------------------------------------------

  def parseHeader (self) :

    for idx in range ( 0, len (self.header) ) :

      line = self.header [idx]

      if ( not line or line.startswith ( "%") ) :
        continue

      ok = re.search ( "^@Relation", line, re.IGNORECASE )

      if ok :
        text = line [ len ( "@Relation" ) + 1 : ]
        attr = text.strip ()
        self.relation = attr
        continue

      ok = re.search ( "^@Attribute", line, re.IGNORECASE )

      if not ok :
        continue

      text = line [ len ( "@Attribute" ) + 1 : ]
      attr = text.strip ()

      name = ""

      if attr.startswith ( "\'" ) :
        text  = attr [ 1 : len (attr) ]

        idx   = text.index ( "'" )
        name  = text [ 0 : idx ]
        value = text [ idx + 1 : ]

      if attr.startswith ( '"' ) :
        text  = attr [ 1 : ]    # skip first character

        idx   = text.index ( '"' )
        name  = text [ 0 : idx ]
        value = text [ idx + 1 : ]

      if ( len (name) == 0 ) :
        sep = '\t'

        if ( not sep in attr ) :
          sep = " "

        idx = attr.index (sep)

        name  = attr [ 0 : idx ]
        value = attr [ idx + 1 : ]

      name  = name.strip ()
      value = value.strip ()

      self.attrNames.append (name)

      info : dict = { "name" : name, "arffType" : value }

      self.attributes.append (info)


  #-------------------------------------------------------------------------
  #
  #  Member function :  readFile  of  ArffConv
  #
  #  Description :
  #
  #   This  function reads  and parses  the  header fields  from the  arff
  #   content.
  #
  #-------------------------------------------------------------------------

  def readFile (self) :

    self.header   = []
    self.dataList = []

    ok, buf = self.fileUtils.readFile ()

    if not ok :
      return False

    bufLen = len (buf)

    found = False

    for i in range ( 0, bufLen ) :

      line = buf [i]

      if not found :
        ok = re.search ( "^@Data", line, re.IGNORECASE )

        if ok :
          self.header = buf [ 0 : i ]    # or buf.slice ( 0, i )
          found = True

          continue

      # now check data section
      if ( found and not line.startswith ( "%" ) ) :
        self.dataList.append (line)

    return True


  #-------------------------------------------------------------------------
  #
  #  Member function :  getDataFrame  of  ArffConv
  #
  #  Description :
  #
  #   This function returns the data frame, a pandas dataframe.
  #
  #-------------------------------------------------------------------------

  def getDataFrame (self) -> list :

    return self.dataFrame


  #-------------------------------------------------------------------------
  #
  #  Member function :  convDataFrame  of  ArffConv
  #
  #  Description :
  #
  #   This function converts the data frame  to the string matrix and also
  #   to a list representation in dataList. It is necessary to do it after
  #   an  arff file  is loaded  but also  before it  saved if  any of  the
  #   attributes was changed.
  #
  #-------------------------------------------------------------------------

  def convDataFrame (self) :

    rows = self.strMatrix.nRows ()
    cols = self.strMatrix.nCols ()

    for idx in range ( 0, rows ) :
      dataRow = list ( self.dataFrame.loc [idx] )

      # make sure we have the string representation
      for col in range ( 0, cols ) :
        value = str ( dataRow [col] )
        dataRow [col] = value

      self.strMatrix.setRowList ( dataRow, idx )

    self.dataList = self.strMatrix.toText ()


  #-------------------------------------------------------------------------
  #
  #  Member function :  setDataFrame  of  ArffConv
  #
  #  Description :
  #
  #   This  function takes  and stores  the  given pandas  data frame  and
  #   analyses the dataframe for attributes (columns) and the data type of
  #   the values. The type of the  values like integer, float or object is
  #   then evaluated and converted to  the arff attribute types like REAL,
  #   NUMERIC and categories.
  #
  #   Dataframe types:
  #    float     --> float64
  #    int       --> int64
  #    datetime  --> datetime64 [ns]
  #    string    --> object
  #
  #-------------------------------------------------------------------------

  def setDataFrame ( self, dataFrame ) :

    self.dataFrame  = dataFrame
    self.attrNames  = dataFrame.columns.values.tolist ()
    self.attributes = []

    rows, cols = dataFrame.shape

    self.strMatrix.reset ( rows, cols )

    self.convDataFrame ()

    # dataframe and strMatrix must already exist
    self.convDataType ()

    self.strMatrix.setColLabels (self.attrNames)
    self.strMatrix.setDelimiter (self.delimiter)
    self.strMatrix.setCleanQuotes (True)
    self.dataList = self.strMatrix.toText ()

    self.attrChanged = False


  #-------------------------------------------------------------------------
  #
  #  Member function :  getAttributes  of  ArffConv
  #
  #  Description :
  #
  #   This function returns the attributes as dictionary, the name of the
  #   attribute is the key.
  #
  #-------------------------------------------------------------------------

  def getAttributes (self) -> list :

    return self.attributes


  #-------------------------------------------------------------------------
  #
  #  Member function :  setAttributes  of  ArffConv
  #
  #  Description :
  #
  #   This function sets dictionary for the attributes of the data set.
  #
  #-------------------------------------------------------------------------

  def setAttributes ( self, attributes : list ) :

    self.attributes = attributes


  #-------------------------------------------------------------------------
  #
  #  Member function :  getAttributeNames  of  ArffConv
  #
  #  Description :
  #
  #   This function returns the attribute names as list.
  #
  #-------------------------------------------------------------------------

  def getAttributeNames (self) -> list :

    return self.attrNames


  #-------------------------------------------------------------------------
  #
  #  Member function :  setAttributeNames  of  ArffConv
  #
  #  Description :
  #
  #   This function sets attribute names for the for the data set.
  #
  #-------------------------------------------------------------------------

  def setAttributeNames ( self, attrNames : list ) :

    self.attrNames = attrNames



  #-------------------------------------------------------------------------
  #
  #  Member function :  setAttributeType  of  ArffConv
  #
  #  Description :
  #
  #   This function sets attribute type for the given name.
  #
  #-------------------------------------------------------------------------

  def setAttributeType ( self, attrName : str, attrType : str ) :

    idx = self.attrNames.index (attrName)

    if ( idx < 0 ) :
      return

    info = self.attributes [idx]
    info ["arffType"] = attrType

    self.attrChanged = True

    text = attrType.lower ()

    if not text.startswith ( "date" ) :
      return

    self.convArffType (idx)

    df = self.dataFrame   # reference to dataframe

    datacol  = df [attrName]  # get specific column by name
    dformat  = info ["df dateformat"]    # format of python datetype

    # convert column
    textList = datacol.dt.strftime (dformat)

    self.strMatrix.setColList ( textList, idx )


  #-------------------------------------------------------------------------
  #
  #  Member function :  getData  of  ArffConv
  #
  #  Description :
  #
  #   This function  returns the  data list,  this is  a string  list very
  #   every string contains the values with a delimiter like a comma.
  #
  #-------------------------------------------------------------------------

  def getData (self) -> list :

    return self.dataList


  #-------------------------------------------------------------------------
  #
  #  Member function :  setData  of  ArffConv
  #
  #  Description :
  #
  #   This function takes  the given list and assigns it to the data list,
  #   this is a  string list very every string contains  the values with a
  #   separator like a comma.
  #
  #-------------------------------------------------------------------------

  def setData ( self, datArray : list ) :

    self.dataList = datArray


  #-------------------------------------------------------------------------
  #
  #  Member function :  getDescription  of  ArffConv
  #
  #  Description :
  #
  #   This function returns the description of the data set.
  #
  #-------------------------------------------------------------------------

  def getDescription (self) -> str :

    return self.relation


  #-------------------------------------------------------------------------
  #
  #  Member function :  setDescription  of  ArffConv
  #
  #  Description :
  #
  #   This function sets the description for the for the data set.
  #
  #-------------------------------------------------------------------------

  def setDescription ( self, info : str ) :

    self.relation = info


  #-------------------------------------------------------------------------
  #
  #  Member function :  loadArff  of  ArffConv
  #
  #  Description :
  #
  #   This function  loads a  file in  ARFF format  and stores  the values
  #   (string) in the 'data' matrix (dataframe)
  #
  #-------------------------------------------------------------------------

  def loadArff (self) :

    self.init ()

    ok = self.readFile ()

    if not ok :
      return ok

    self.parseHeader   ()
    self.evalDelimiter ()

    if self.delimiter != "," :      # could be confused with date variables
      msg = "Found wrong delimiter in arff file : " + self.fileName
      print (msg)
      self.delimiter = ","

    self.buildData ()

    self.isValid = ok

    return ok


  #-------------------------------------------------------------------------
  #
  #  Member function :  saveArff  of  ArffConv
  #
  #  Description :
  #
  #   This function  saves data and header in  ARFF format in a file
  #   with the defined filename.
  #
  #-------------------------------------------------------------------------

  def saveArff ( self, fileName : str = "" ) -> bool :

    if ( self.isValid == False ) :
      return False

    if not fileName :
      fileName = self.fileName

    if self.attrChanged :
      self.dataList = self.strMatrix.toText ()

    content = []

    text = "@RELATION " + self.relation + "\n"  # plus empty line
    content.append (text)

    for index in range ( 0, len (self.attributes) ) :

      info = self.attributes [index]

      value = info ["arffType"]
      name  = info ["name"]

      if value == "date" :
        text = ' "' + info ["ARFF dateformat"] + '"'
        value = value + text

      text  = "@ATTRIBUTE " + name + " " + value
      content.append (text)

    text = "\n@DATA"
    content.append (text)

    content.extend ( self.dataList )

    self.fileUtils.setFileName (fileName)
    self.fileUtils.writeFile (content)

    return True


  #-------------------------------------------------------------------------
  #
  #  Member function :  saveDataFrame  of  ArffConv
  #
  #  Description :
  #
  #   This function  saves data and header in  ARFF format in a file
  #   with the defined filename.
  #
  #  Output parameter :
  #   success         : Success, true or false
  #
  #-------------------------------------------------------------------------

  def saveDataFrame ( self, fileName : str = "" ) :

    if ( self.isValid == False ) :
      return False

    if not fileName :
      fileName = self.fileName

    self.dataFrame.to_csv ( fileName, index = False, sep = self.delimiter )


  #-------------------------------------------------------------------------
  #
  #  Member function :  setFileName  of  ArffConv
  #
  #  Description :
  #
  #   This function sets member variable 'fileName' to the given value.
  #
  #  Input parameter  :
  #   fileName        : new value for member variable fileName
  #
  #-------------------------------------------------------------------------

  def setFileName ( self, fileName : str ) :

    self.fileName = fileName

    self.fileUtils.setFileName (fileName)


