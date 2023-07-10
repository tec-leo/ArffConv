#-------------------------------------------------------------------------
#
#  File Name   :  StringUtils
#
#  Description :
#
#   This module contains helper and utility functions for strings.
#
#  Developer : Oskar Leirich                Creation date : 11.Dec.2016
#  Modified  : Oskar Leirich                Last changes  : 18.Jan.2023
#
#  This unit contains following functions :
#   of StringUtils :
#    chomp                replace
#
#-------------------------------------------------------------------------

import re
import csv


#-------------------------------------------------------------------------
#
#  Function name :  chomp  of  StringUtils
#
#  Description :
#
#   This function  removes any trailing  string that corresponds  to the
#   'trail' value and returns it as new string.
#
#  Input parameter  :
#   inStr           : input string
#
#  Output parameter :
#   (str)           : output string
#
#-------------------------------------------------------------------------

def chomp ( inStr : str, trail : str = "\n" ) -> str :

  rep = trail + "+$"    # all occurrences at the end

  outStr: str = replace (  inStr, rep, "" )

  return outStr


#-------------------------------------------------------------------------
#
#  Function name :  getDelimiter
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
#
#-------------------------------------------------------------------------

def getDelimiter ( inList : list ) :

  dialect = getDialect (inList)

  delim  = dialect.delimiter

  return delim


#-------------------------------------------------------------------------
#
#  Function name :  getDialect  of  StringUtils
#
#  Description :
#
#   This function  uses the class  'csv.Sniffer' to guess the  format of
#   the given  string list. It does  not work directly with  a csv file,
#   therefore it cannot guess things like header, line endings etc.
#
#  Input parameter  :
#   inList          : input string
#
#  Output parameter :
#   (Dialect)       : csv dialect with some information like delimiter
#
#-------------------------------------------------------------------------

def getDialect ( inList : list ) -> csv.Dialect :

  text = "\n".join (inList)

  sniffer = csv.Sniffer ()
  dialect = sniffer.sniff (text)

  return dialect


#-------------------------------------------------------------------------
#
#  Member function :  isFloat  of  StringUtils
#
#  Description :
#
#   This  function checks  if the  given string  can be  converted to  a
#   floating point  value. Be  careful also an  integer variable  can be
#   sometimes be converted to a floating point value.
#
#  Input parameter  :
#   testStr         : string to test
#
#  Output parameter :
#   (bool)          : success (true) or not
#
#-------------------------------------------------------------------------

def isFloat ( testStr : str ) -> bool :

  try:
    val = float (testStr)

    return True

  except ValueError:
    return False


#-------------------------------------------------------------------------
#
#  Member function :  isInt  of  StringUtils
#
#  Description :
#
#   This function  checks if  the given  string can  be converted  to an
#   integer value. Be careful also a  float variable can be sometimes be
#   converted to an integer value.
#
#  Input parameter  :
#   testStr         : string to test
#
#  Output parameter :
#   (bool)          : success (true) or not
#
#-------------------------------------------------------------------------

def isInt ( testStr : str ) -> bool :

  try:
    val = int (testStr)

    return True

  except ValueError:
    return False


#-------------------------------------------------------------------------
#
#  Function name :  replace  of  StringUtils
#
#  Description :
#
#   This function replaces the  given regex pattern (regular expression)
#   with the replacement and returns it as new string.
#
#  Input parameter  :
#   inStr           : input string
#   pattern         : pattern string (regular expression)
#   replStr         : replacement string
#
#  Output parameter :
#   (str)           : output string
#
#-------------------------------------------------------------------------

def replace ( inStr : str, pattern : str, replStr : str ) -> str :

  outStr : str = re.sub ( pattern, replStr, inStr )

  return outStr


#-------------------------------------------------------------------------
#
#  Function name : trimmed
#
#  Description :
#
#   This function deletes whitespaces at the beginning and at the end of
#   the given string.
#
#-------------------------------------------------------------------------*/

def trimmed ( inStr : str ) -> str :

  outStr : str = inStr.strip ()

  return outStr
