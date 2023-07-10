#-------------------------------------------------------------------------
#
#  PrepArff
#
#  Description :
#
#   This module  reads some pandas dataframes and combines properties and labels.
#   The result is then written as arff file and also as csv file.
#
#
#  Developer : Oskar Leirich                Creation date : 14.Jan.2023
#  Modified  : Oskar Leirich                Last changes  : 14.Jan.2023
#
#-------------------------------------------------------------------------

#!/usr/bin/env python
# coding: utf-8

import sys
import arff

# Common imports
import numpy as np
import os
import pandas as pd

cat_ver = 0
cat_hor = 1

HOUSING_PATH = os.path.join ( "datasets", "housing" )

prep_path  = os.path.join ( HOUSING_PATH, "housing_prep.csv" )
label_path = os.path.join ( HOUSING_PATH, "housing_labels.csv" )
col_path   = os.path.join ( HOUSING_PATH, "housing_columns.csv" )

#df_prepared = pd.read_csv (prep_path)
#df_labels   = pd.read_csv (label_path)
df_columns  = pd.read_csv ( col_path, sep = "," )

np_prepared = np.loadtxt ( prep_path, dtype="float", comments="#", delimiter="," )
np_labels   = np.loadtxt ( label_path, dtype="float", comments="#", delimiter="," )

df_labels   = pd.DataFrame ( np_labels, columns= [ "Labels" ] )
df_housing  = pd.DataFrame ( np_prepared, columns=df_columns.columns )

df_house1   = pd.concat ( [ df_housing, df_labels ], cat_hor )

# add labels
df_housing [ "Labels" ] = df_labels [ "Labels" ]

cols = df_housing.shape [1]
attributes = []

# get columns names as string list - both versions work
names = list (df_housing)
names = df_housing.columns.values.tolist ()

for idx in range ( 0, cols ) :
  entry = ( names [idx], "numeric" )
  attributes.append (entry)

# convert numpy array to list of lists
numArray = df_housing.to_numpy ()
houseArray = numArray.tolist()

arff_dic = {
  'description': 'Prepared housing data of ML Praxis',
  'relation': 'Housing',
  'attributes': attributes,
  'data': houseArray
}

# write csvfile
prep_path  = os.path.join ( HOUSING_PATH, "housingPrep.csv" )
#df_housing.to_csv ( prep_path, sep='\t' )

# write (dump) arff file
hfile = open ( "Housing.arff", "w", encoding="utf8" )

#arff.dump ( arff_dic, houseArray, attributes=attributes, names = names, relation = "Housing" )

#arff.dump ( arff_dic, hfile )
content = arff.dumps ( arff_dic )

hfile.close ()
