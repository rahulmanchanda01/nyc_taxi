# -*- coding: utf-8 -*-
"""
Created on Tue Aug 09 23:04:37 2016

@author: surag
"""

#==============================================================================
# Import required libraries
#==============================================================================
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os 
from uszipcode import ZipcodeSearchEngine
search = ZipcodeSearchEngine()

#==============================================================================
# Set seed and parameters for randomsampling
#==============================================================================
np.random.seed(456)
nlinesrandomsample = 100000
nlines = list([13158262,12324935,11562783,11130304,11225063,12315488,11312676,\
                1048575])
files = os.listdir('Datasets')

#==============================================================================
# Initialize empty dataset
#==============================================================================
nyc_taxi_may_dec2015 = pd.DataFrame()

#==============================================================================
# Load the datasets from each file and append onto one file.
#==============================================================================
for i in range(8):
    lines2skip = np.random.choice(np.arange(1,nlines[i]+1), \
    (nlines[i]-nlinesrandomsample), replace=False)
    nyc_taxi_temp = pd.read_csv('Datasets/'+files[i],skiprows = lines2skip)
    nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.append(nyc_taxi_temp) 

#==============================================================================
# Function to extract Zipcodes from coordinates    
#==============================================================================
def cordnts_zip(a,b):
    try:
        location = search.by_coordinate(a,b)
        lctn_zip = location[0]["Zipcode"]
    except:
        lctn_zip = ''
    return lctn_zip

#==============================================================================
# Remove temporary variables
#==============================================================================
del nyc_taxi_temp,nlines,lines2skip,i,files,nlinesrandomsample

#==============================================================================
# Convert datetime object column to datetime series
#==============================================================================
nyc_taxi_may_dec2015['tpep_pickup_datetime'] = pd.to_datetime(\
                nyc_taxi_may_dec2015['tpep_pickup_datetime'])

#==============================================================================
# Extract month, time and day from Timestamp
#==============================================================================
nyc_taxi_may_dec2015['Month'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.month
nyc_taxi_may_dec2015['Time'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.time
nyc_taxi_may_dec2015['Day'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.day

#==============================================================================
# Remove erroneoys coordinates (0,0) from the dataset
#==============================================================================
nyc_taxi_may_dec2015 = \
nyc_taxi_may_dec2015[(nyc_taxi_may_dec2015['pickup_latitude'] != 0 ) & \
(nyc_taxi_may_dec2015['pickup_longitude']!=0 )]  

#==============================================================================
# Set index for the dataset to be unique
#==============================================================================
nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.set_index(np.arange(0,788757))

#==============================================================================
# Add columns for Pick-up and drop-off zipcodes
#==============================================================================
nyc_taxi_may_dec2015['pickup_zip'] = nyc_taxi_may_dec2015.apply(lambda x:\
cordnts_zip(x['pickup_latitude'],x['pickup_longitude']),axis=1)   

nyc_taxi_may_dec2015['dropoff_zip'] = nyc_taxi_may_dec2015.apply(lambda x:\
cordnts_zip(x['dropoff_latitude'],x['dropoff_longitude']),axis=1)                 
                        
#==============================================================================
# nyc_taxi_may_dec2015.to_csv('nyc_taxi_may_dec2015.csv')
#==============================================================================
#==============================================================================
# Run only to load the file from this point onwards                        
# nyc_taxi_may_dec2015 = pd.read_csv('nyc_taxi_may_dec2015.csv')
#==============================================================================
