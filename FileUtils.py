#-------------------------------------------------------------------------
#
#  File Name   :  FileUtils
#
#  Description :
#
#   This module provides the class 'FileUtils' which contains helper and
#   utility functions to load text files and store all lines in a string
#   array in several  orientations. It contains also  functions to check
#   the file type, files and a lot of more.
#
#  Developer : Oskar Leirich                Creation date : 11.Dec.2016
#  Modified  : Oskar Leirich                Last changes  : 18.Jan.2023
#
#
#  This class contains following member functions :
#   of FileUtils :
#    FileUtils                 ~FileUtils                cleanFileName
#    findFile                  getBaseNames
#    getFile                   getFileName               getSize
#    readFile                  readLine                  setFileName
#    writeFile
#
#-------------------------------------------------------------------------

import fnmatch
import os
import os.path
import StringUtils as strUtils


#-------------------------------------------------------------------------
#
#  Class Name   :  FileUtils.cpp
#
#  Description :
#
#   This class contains helper and  utility functions to load text files
#   and store all lines in a string list.
#
#-------------------------------------------------------------------------

class FileUtils (object) :

  def __init__ (self) :

    self.fileName = ""
    self.hfile    = None


  #-------------------------------------------------------------------------
  #
  #  Member function :  findRecursive  of  FileUtils
  #
  #  Description :
  #
  #   This function  searches from  the given start  directory recursively
  #   for  all files  with  the given  fileSpec  (regular expression)  and
  #   returns all  found files in  a string  list which contains  the full
  #   path over every match.
  #
  #  Input parameter  :
  #   nameFilters     : file name filter (regular expression)
  #   startDir        : start directory list of directories to search
  #
  #  Output parameter :
  #   (list)          : final list of found files
  #
  #-------------------------------------------------------------------------

  @staticmethod
  def findRecursive (nameFilters: list, startDir: str)  -> list :

    filters = []

    for x in nameFilters :
      regex = fnmatch.translate (x)
      filters.append (regex)

    foundList = []

    for root, dirs, filenames in os.walk (startDir) :

      for extensions in nameFilters :

        for filename in fnmatch.filter ( filenames, extensions ) :
          name = os.path.join ( root, filename )
          name = name.replace ( "\\", "/" )

          foundList.append ( name )

    return foundList


  #-------------------------------------------------------------------------
  #
  #  Member function :  closeFile  of  FileUtils
  #
  #  Description :
  #
  #   This function closes the file if it is open and sets the file handle
  #   to none.
  #
  #-------------------------------------------------------------------------

  def closeFile (self) :

    if self.hfile is not None :
      self.hfile.close ()
      self.hfile = None


  #-------------------------------------------------------------------------
  #
  #  Member function :  readFile  of  FileUtils
  #
  #  Description :
  #
  #   This function is the starting point for reading the text file into a
  #   string array.
  #
  #  Input parameter  :
  #   content         : String list containing all lines of the file
  #   chomp_nl        : true - remove trailing newlines
  #
  #  Output parameter :
  #   success         : Success, true or false
  #
  #  Note:
  #   Pass by value     : string, integer, tuple
  #   Pass by reference : list, set, dictionary
  #
  #-------------------------------------------------------------------------

  def readFile ( self, chomp_nl : bool = True ) :

    self.closeFile ()    # close if open

    content = []

    try :
      self.hfile = open ( self.fileName, "r", encoding = "utf8" )

      content = self.hfile.readlines ()

      self.closeFile ()    # close if open

      if chomp_nl :        # remove trailing newlines
        for idx in range ( 0, len (content) ) :

          line = strUtils.chomp ( content [idx] )
          content [idx] = line


      return True, content

    except ( FileNotFoundError, PermissionError, OSError ) :
      msg = "Cannot open file : " + self.fileName + " for reading !"
      print (msg)

    return False, content


  #-------------------------------------------------------------------------
  #
  #  Member function :  writeFile  of  FileUtils
  #
  #  Description :
  #
  #   This function writes  the given string list as a  text file with the
  #   name given to self class when creating it.
  #
  #  Input parameter  :
  #   content         : String list containing all lines of the file
  #   append          : Open in AppendMode (True) or WriteOnly (default)
  #   with_nl         : add new line to every string before writing it
  #
  #  Output parameter :
  #   success         : Success, true or false
  #
  #------------------------------------------------------------------------

  def writeFile ( self, content : list, append : bool = False,
                  with_nl : bool = True ) -> bool :

    try :

      if append :
        self.hfile = open ( self.fileName, "a", encoding = "utf8" )
      else :
        self.hfile = open ( self.fileName, "w", encoding = "utf8" )

      if with_nl :        # remove trailing newlines
        for idx in range ( 0, len (content) ) :

          line = content [idx] + "\n"
          content [idx] = line

      self.hfile.writelines (content)

      self.closeFile ()    # close if open

    except ( FileNotFoundError, PermissionError, OSError ) :
      msg = "Cannot open file : " + self.fileName + " for writing !"
      print (msg)

      return False

    return True


  #-------------------------------------------------------------------------
  #
  #  Member function :  setFileName  of  FileUtils
  #
  #  Description :
  #
  #   This function sets member variable 'fileName' to the given value.
  #
  #  Input parameter  :
  #   fileName        : new value for member variable fileName
  #
  #-------------------------------------------------------------------------

  def setFileName ( self, fileName ) :

    self.fileName = fileName

    self.closeFile ()    # close if open
