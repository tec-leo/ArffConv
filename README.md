# ArffConv

## Overview

The python module "ArffConv" contains the class "ArffConv" which implements functions
 to read and write ARFF files and to convert between ARFF and a pandas dataframe.

ARFF (Attribute-Relation File Format) is a file format for datasets which are
commonly used for machine learning experiments and software.
This file format was created to be used in Weka, a representative software for
machine learning automated experiments.


The Weka home page is in [Weka](https://www.cs.waikato.ac.nz/ml/weka/).
ARFF is described in [Weka Wiki](https://waikato.github.io/weka-wiki/formats_and_processing/arff_developer/).


## Features

* loadArff - loads an ARFF file
* saveArff - write content into an ARFF file
* saveDataFrame - write content as csv file with comma as delimiter
* setDataFrame - reads the content from a panda dataframe

## How to use

Clone this repository into your project.

    git clone https://www.github.com/tec-leo/ArffConv.git

Typical use case is creating a class instance and then loading an ARFF file or initializing  it with a pandas dataframe from a python script.

    import ArffConv

    arff = ArffConv.ArffConv ()

    arff.setFileName ( "Data.arff" )
    arff.loadArff ()
    arff.saveDataFrame ( "Data-df.csv" )
    arff.setDescription ( "Just a test data set" )
    arff.saveArff ( "DataTest.arff" )

## Examples

The python module "ArffTest" contains some test cases and examples,

## Bug and Features

If you find a bug please make an issue and attach the problematic file(s).
If you think a helpful feature is missing please also make an issue and
I will try to implement it.

## License
GPL License Version 3

see License.txt in this directory

