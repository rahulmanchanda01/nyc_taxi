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
from uszipcode import ZipcodeSearchEngine
search = ZipcodeSearchEngine()
import plotly.plotly as py
py.sign_in('suryak1210', 'nd72ait1tg')

geolocator = Nominatim()

#def cordnts_zip(a,b):
#    cordnts = str(a) + ',' + str(b)
#    location = geolocator.reverse(cordnts)
#    lctn_zip = int(location.raw['address']['postcode'][0:5])
#    return lctn_zip

#def cordnts_zip(a,b):
#    location = geocoder.google([a,b],method ="reverse")
#    lctn_zip = location.postal
#    return lctn_zip

def cordnts_zip(a,b):
    location = search.by_coordinate(a,b)
    lctn_zip = location[0]["Zipcode"]
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

nyc_taxi_may_dec2015['dropoff_location_zip'] = nyc_taxi_may_dec2015.apply(lambda x : 
    cordnts_zip(x['dropoff_latitude'],x['dropoff_longitude']),axis=1)

nyc_taxi_trial = nyc_taxi_may_dec2015.head(1)

### Merging zip codes data set
zip_codes = pd.read_csv('zips.csv')
nyc_taxi_may_dec2015_zip = pd.merge(nyc_taxi_may_dec2015,zip_codes,\
 left_on=['pickup_latitude','pickup_longitude'], \
 right_on=['latitude','longitude] )

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


P=nyc_taxi_may_dec2015.plot(kind='scatter', x='dropoff_longitude', \
        y='dropoff_latitude',color='white',\
        xlim=(-74.06,-73.77),ylim=(40.61, 40.91),s=.02,alpha=.6)
P.set_axis_bgcolor('#800000') #Background Color

a = list(nyc_taxi_may_dec2015['pickup_latitude'].head(10000))
b = list(nyc_taxi_may_dec2015['pickup_longitude'].head(10000))
#### Scatter plot

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = nyc_taxi_may_dec2015['pickup_longitude'].head(10000) ,
        lat = nyc_taxi_may_dec2015['pickup_latitude'].head(10000),
#        text = df['text'],
        mode = 'markers',
        marker = dict( 
            size = 8, 
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = 0,
            color = df['cnt'],
            cmax = df['cnt'].max(),
            colorbar=dict(
                title="Pickup Location"
            )
        ))]

layout = dict(
        title = 'NYC TAXI',
        colorbar = True,   
        geo = dict(
            scope='NY',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5        
        ),
    )

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False)
