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
import gmplot
import geocoder 

geolocator = Nominatim()

#def cordnts_zip(a,b):
#    cordnts = str(a) + ',' + str(b)
#    location = geolocator.reverse(cordnts)
#    lctn_zip = int(location.raw['address']['postcode'][0:5])
#    return lctn_zip

def cordnts_zip(a,b):
    location = geocoder.google([a,b],method ="reverse")
    lctn_zip = location.postal
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

### Plottong pickup locations
     
new_style = {'grid': False} #Remove grid   
from matplotlib import rcParams  
rcParams['figure.figsize'] = (17.5, 17) #Size of figure  
rcParams['figure.dpi'] = 250


P=nyc_taxi_may_dec2015.plot(kind='scatter', x='pickup_longitude', y='pickup_latitude',color='white',\
        xlim=(-74.06,-73.77),ylim=(40.61, 40.91),s=.02,alpha=.6)
P.set_axis_bgcolor('#800000') #Background Color

### Plottong pickup locations
 
new_style = {'grid': False} #Remove grid   
from matplotlib import rcParams  
rcParams['figure.figsize'] = (17.5, 17) #Size of figure  
rcParams['figure.dpi'] = 250


P=nyc_taxi_may_dec2015.plot(kind='scatter', x='dropoff_longitude', y='dropoff_latitude',color='white',\
        xlim=(-74.06,-73.77),ylim=(40.61, 40.91),s=.02,alpha=.6)
P.set_axis_bgcolor('#800000') #Background Color

#m = Basemap(projection='mill',llcrnrlat=20,urcrnrlat=50,\
#            llcrnrlon=-130,urcrnrlon=-60,resolution='c')
#fig = plt.figure()
#themap = Basemap(projection='gall',llcrnrlat=35.,urcrnrlat=50,\
#                llcrnrlon=-130,urcrnrlon=-60,resolution='l')

#themap.drawcoastlines()
#themap.drawcountries()
#themap.fillcontinents(color = 'yellow')
#themap.drawmapboundary(fill_color='blue')
#
#a = nyc_taxi_may_dec2015['pickup_longitude'].head(25)
#b = nyc_taxi_may_dec2015['pickup_latitude'].head(25)
#
#for x1,y1 in zip(a,b):
#    x, y = themap(x1,y1)               
#    themap.plot(x, y, 
#                'o',                    # marker shape
#                color='red',         # marker colour
#                markersize=5           # marker size
#                )
#    
#plt.show()