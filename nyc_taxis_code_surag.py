# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 03:20:29 2016

@author: SuryaNarayana
"""

#Import required libraries
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os 
from uszipcode import ZipcodeSearchEngine
search = ZipcodeSearchEngine()

#Set seed and parameters for randomsampling
np.random.seed(456)
nlinesrandomsample = 100000
nlines = list([13158262,12324935,11562783,11130304,11225063,12315488,11312676,\
                1048575])
files = os.listdir('Datasets')

##Initialize empty dataset
nyc_taxi_may_dec2015 = pd.DataFrame()

##Load the datasets from each file and append onto one file.
for i in range(8):
    lines2skip = np.random.choice(np.arange(1,nlines[i]+1), \
    (nlines[i]-nlinesrandomsample), replace=False)
    nyc_taxi_temp = pd.read_csv('Datasets/'+files[i],skiprows = lines2skip)
    nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.append(nyc_taxi_temp) 
    
nyc_zips = pd.read_csv('zips.csv')
def cordnts_zip(a,b):
    try:
        location = search.by_coordinate(a,b)
        lctn_zip = location[0]["Zipcode"]
    except:
        lctn_zip = ''
    return lctn_zip

##Remove temporary variables
del nyc_taxi_temp,nlines,lines2skip,i,files,nlinesrandomsample

##Convert datetime object column to datetime series
nyc_taxi_may_dec2015['tpep_pickup_datetime'] = pd.to_datetime(\
                nyc_taxi_may_dec2015['tpep_pickup_datetime'])

nyc_taxi_may_dec2015['Month'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.month
nyc_taxi_may_dec2015['Time'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.time
nyc_taxi_may_dec2015['Day'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.day

nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015[(nyc_taxi_may_dec2015['pickup_latitude'] != 0 ) \
                        & (nyc_taxi_may_dec2015['pickup_longitude']!=0 )]  
nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.set_index(np.arange(0,788757))                        
                        
nyc_taxi100k = nyc_taxi_may_dec2015[0:100000]
nyc_taxi100_200k = nyc_taxi_may_dec2015[100000:200000]
nyc_taxi200k_end = nyc_taxi_may_dec2015[200000:788757]

nyc_taxi100k['pickup_zip'] = nyc_taxi100k.apply(lambda x : 
    cordnts_zip(x['pickup_latitude'],x['pickup_longitude']),axis=1)   
nyc_taxi100_200k['pickup_zip'] = nyc_taxi100_200k.apply(lambda x : 
    cordnts_zip(x['pickup_latitude'],x['pickup_longitude']),axis=1)
nyc_taxi200k_end['pickup_zip'] = nyc_taxi200k_end.apply(lambda x : 
    cordnts_zip(x['pickup_latitude'],x['pickup_longitude']),axis=1)  

nyc_taxi100k.to_csv('nyc_taxi100k.csv')
nyc_taxi100_200k.to_csv('nyc_taxi100_200k.csv')
nyc_taxi200k_end.to_csv('nyc_taxi200k_end.csv')   

nyc_final = nyc_taxi100k.append(nyc_taxi100_200k).append(nyc_taxi200k_end)
nyc_final.to_csv('nyc_final.csv')

nyc_final['dropoff_zip'] = nyc_final.apply(lambda x : 
    cordnts_zip(x['dropoff_latitude'],x['dropoff_longitude']),axis=1)  


nyc_taxi_may_dec2015 = pd.read_csv('Final Dataset/nyc_taxi_may_dec2015.csv')
nyc_taxi_may_dec2015['pickup_latitude1'] = pd.to_numeric(nyc_taxi_may_dec2015['pickup_latitude']).round(3)
nyc_taxi_may_dec2015['pickup_longitude1'] = pd.to_numeric(nyc_taxi_may_dec2015['pickup_longitude']).round(3)
nyc_zips['latitude1'] = pd.to_numeric(nyc_zips['latitude']).round(3)
nyc_zips['longitude1'] = pd.to_numeric(nyc_zips['longitude']).round(3)
nyc_taxi_may_dec2015_zips = pd.merge(nyc_taxi_may_dec2015,nyc_zips,left_on = ['pickup_latitude1','pickup_longitude1'],right_on = ['latitude1','longitude1'])