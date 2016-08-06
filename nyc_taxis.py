# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 03:20:29 2016

@author: SuryaNarayana
"""
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

nlinesfile = 11460573
nlinesrandomsample = 50000
lines2skip = np.random.choice(np.arange(1,nlinesfile+1), \
(nlinesfile-nlinesrandomsample), replace=False)
np.random.seed()

nyc_taxi_12 = pd.read_csv('yellow_tripdata_2015-12.csv',skiprows=lines2skip)    
nyc_taxi_11 = pd.read_csv('yellow_tripdata_2015-11.csv',skiprows=lines2skip) 
nyc_taxi_10 = pd.read_csv('yellow_tripdata_2015-10.csv',skiprows=lines2skip) 
nyc_taxi_09 = pd.read_csv('yellow_tripdata_2015-09.csv',skiprows=lines2skip) 
nyc_taxi_08 = pd.read_csv('yellow_tripdata_2015-08.csv',skiprows=lines2skip) 
nyc_taxi_07 = pd.read_csv('yellow_tripdata_2015-07.csv',skiprows=lines2skip) 
nyc_taxi_06 = pd.read_csv('yellow_tripdata_2015-06.csv',skiprows=lines2skip) 

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