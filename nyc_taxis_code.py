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
import os 
from geopy.geocoders import Nominatim
geolocator = Nominatim()

def cordnts_zip(a,b):
    cordnts = str(a) + ',' + str(b)
    location = geolocator.reverse(cordnts)
    lctn_zip = int(location.raw['address']['postcode'][0:5])
    return lctn_zip

np.random.seed(456)
nlinesrandomsample = 100000
nlines = list([13158262,12324935,11562783,11130304,11225063,12315488,11312676,\
                1048575])
files = os.listdir('Datasets')

nyc_taxi_may_dec2015 = pd.DataFrame()

for i in range(8):
    lines2skip = np.random.choice(np.arange(1,nlines[i]+1), \
    (nlines[i]-nlinesrandomsample), replace=False)
    nyc_taxi_temp = pd.read_csv('Datasets/'+files[i],skiprows = lines2skip)
    nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.append(nyc_taxi_temp) 

del nyc_taxi_temp,nlines,lines2skip,i,files,nlinesrandomsample

nyc_taxi_may_dec2015['tpep_pickup_datetime'] = pd.to_datetime(\
                nyc_taxi_may_dec2015['tpep_pickup_datetime'])

nyc_taxi_may_dec2015['Month'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.month
nyc_taxi_may_dec2015['Time'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.time
nyc_taxi_may_dec2015['Day'] = nyc_taxi_may_dec2015['tpep_pickup_datetime'].dt.day
nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015.set_index(np.arange(0,800000))
nyc_taxi_may_dec2015 = nyc_taxi_may_dec2015[(nyc_taxi_may_dec2015['pickup_latitude'] != 0 ) \
                        & (nyc_taxi_may_dec2015['pickup_longitude']!=0 )]

nyc_taxi_may_dec2015['location_zip'] = nyc_taxi_may_dec2015.apply(lambda x : 
    cordnts_zip(x['pickup_latitude'],x['pickup_longitude']),axis=1)

pickup_loc = np.array([nyc_taxi_12['pickup_longitude'],nyc_taxi_12['pickup_latitude']]) 

a = nyc_taxi_may_dec2015[93:94][['pickup_latitude','pickup_longitude']]
a['location_zip'] = a.apply(lambda x : 
    cordnts_zip(x['pickup_latitude'],x['pickup_longitude']),axis=1)
    
fig = plt.figure()

themap = Basemap(projection='gall',
              llcrnrlon = -40.917577,              # lower-left corner longitude
              llcrnrlat = -74.25909,               # lower-left corner latitude
              urcrnrlon = 40.917577,               # upper-right corner longitude
              urcrnrlat = -74.25909,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )
themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')

x, y = themap(pickup_loc[0],pickup_loc[1])
themap.plot(x, y, 
                'o',                    # marker shape
               color='Indigo',         # marker colour
               markersize=4            # marker size
               )
plt.show()