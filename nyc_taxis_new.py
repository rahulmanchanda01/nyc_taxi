# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 03:20:29 2016

@author: Surag
"""
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os

np.random.seed(456)
nlinesrandomsample = 100000

nlines = list([13158262,12324935,11562783,11130304,11225063,12315488,11312676,1048575])
files = os.listdir('Datasets')

nyc_taxi_may_dec2015 = pd.DataFrame()

for i in range(8):
    lines2skip = np.random.choice(np.arange(1,nlines[i]+1), \
(nlines[i]-nlinesrandomsample), replace=False)
    nyc_taxi_temp = pd.read_csv('Datasets/'+files[i],skiprows = lines2skip)
    nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.append(nyc_taxi_temp)
    del nyc_taxi_temp
    
nyc_taxi_may_dec2015['tpep_pickup_datetime'] = pd.to_datetime(nyc_taxi_may_dec2015['tpep_pickup_datetime'])

nyc_taxi_may_dec2015['year'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.year

a=2
#nyc_taxi_may_dec2015.to_csv('Final dataset/nyc_taxi_may_dec2015.csv')
#==============================================================================
# nyc_taxi_12 = pd.read_csv('Datasets/yellow_tripdata_2015-12.csv')
# nyc_taxi_11 = pd.read_csv('Datasets/yellow_tripdata_2015-11.csv')
# nyc_taxi_10 = pd.read_csv('Datasets/yellow_tripdata_2015-10.csv') 
# 
# nyc_taxi_09 = pd.read_csv('Datasets/yellow_tripdata_2015-09.csv') 
# nyc_taxi_08 = pd.read_csv('Datasets/yellow_tripdata_2015-08.csv') 
# nyc_taxi_07 = pd.read_csv('Datasets/yellow_tripdata_2015-07.csv') 
# nyc_taxi_06 = pd.read_csv('Datasets/yellow_tripdata_2015-06.csv') 
# nyc_taxi_05 = pd.read_csv('Datasets/yellow_tripdata_2015-05.csv') 
#==============================================================================
#pickup_loc = np.array([nyc_taxi_12['pickup_longitude'],nyc_taxi_12['pickup_latitude']]) 
#
#fig = plt.figure()
#
#themap = Basemap(projection='gall',
#              llcrnrlon = -40.917577,              # lower-left corner longitude
#              llcrnrlat = -74.25909,               # lower-left corner latitude
#              urcrnrlon = 40.917577,               # upper-right corner longitude
#              urcrnrlat = -74.25909,               # upper-right corner latitude
#              resolution = 'l',
#              area_thresh = 100000.0,
#              )
#themap.drawcoastlines()
#themap.drawcountries()
#themap.fillcontinents(color = 'gainsboro')
#themap.drawmapboundary(fill_color='steelblue')
#
#x, y = themap(pickup_loc[0],pickup_loc[1])
#themap.plot(x, y, 
#                'o',                    # marker shape
#               color='Indigo',         # marker colour
#               markersize=4            # marker size
#               )
#plt.show()