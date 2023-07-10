# -------------------------------------------------------------------------
#
#  Class       :  ArffTest
#
#  Description :
#
#   This module contains test cases for the class 'ArffConv'.
#
#
#  Developer : Oskar Leirich                Creation date : 16.Jan.2023
#  Modified  : Oskar Leirich                Last changes  : 10.Jul.2023
#
#
# -------------------------------------------------------------------------

import ArffConv

arff = ArffConv.ArffConv ()

# several test cases
testcases = [ 1, 2, 3, 4 ]
testcases = [ 4 ]

if ( 1 in testcases ) :    # weather data
  arff.setFileName ( "Data/weather.arff" )
  arff.loadArff ()
  arff.saveDataFrame ( "Test/weather.csv" )
  arff.setDescription ( "Just a test data set" )
  arff.saveArff ( "Test/weather-1.arff" )

  df = arff.getDataFrame ()
  arff.setDataFrame (df)

  arff.saveDataFrame ( "Test/weather-df.csv" )

  arff.saveArff ( "Test/weather-from-df.arff" )

if ( 2 in testcases ) :    # test with simple data time
  arff.setFileName ( "Data/DataTime.arff" )
  arff.loadArff ()
  arff.saveDataFrame ( "Test/DataTime.csv" )

  df = arff.getDataFrame ()
  arff.setDataFrame (df)

  arff.saveDataFrame ( "Test/DataTime-from-df.csv" )

  arff.saveArff ( "Test/DataTime-from-df.arff" )

if ( 3 in testcases ) :    # test with dates and times
  arff.setFileName ( "Data/DateMay.arff" )
  arff.loadArff ()
  arff.saveDataFrame ( "Test/DateMay.csv" )

  df = arff.getDataFrame ()
  arff.setDataFrame (df)

  arff.saveDataFrame ( "Test/DateMay-df.csv" )
  arff.saveArff ( "Test/DateMay-3.arff" )

  arff.setAttributeType ( "Date",      "DATE dd.MM.yyyy" )
  arff.setAttributeType ( "Sunrise",   "DATE HH:mm" )
  arff.setAttributeType ( "Sunset",    "DATE dd-MM-yyyy HH:mm" )
  arff.setAttributeType ( "Daylength", "DATE HH:mm" )

  arff.saveDataFrame ( "Test/DateMay-attr.csv" )
  arff.saveArff ( "Test/DateMay-attr.arff" )

if ( 4 in testcases ) :    # iris data set with weight and sparse matrix
  arff.setFileName ( "Data/iris-weight.arff" )
  arff.loadArff ()
  arff.saveDataFrame ( "Test/iris-weight.csv" )
  arff.setDescription ( "No more a sparse data set" )
  arff.saveArff ( "Test/iris-normal.arff" )

  df = arff.getDataFrame ()
  arff.setDataFrame (df)

  arff.saveDataFrame ( "Test/iris-normal-df.csv" )

  arff.saveArff ( "Test/iris-from_df.arff" )

if ( 5 in testcases ) :    # weather data with quotes attributes
  arff.setFileName ( "Data/weather_sep.arff" )
  arff.loadArff ()
  arff.saveDataFrame ( "Test/weather_sep.csv" )
  arff.setDescription ( "Just a test data set" )
  arff.saveArff ( "Test/weather_sep-1.arff" )

  df = arff.getDataFrame ()
  arff.setDataFrame (df)

  arff.saveDataFrame ( "Test/weather_sep-df.csv" )

  arff.saveArff ( "Test/weather_sep-from-df.arff" )

