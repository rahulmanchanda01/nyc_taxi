# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 14:40:05 2016

@author: Pranathi
"""

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os 
from uszipcode import ZipcodeSearchEngine
search = ZipcodeSearchEngine()

np.random.seed(456)
nlinesrandomsample = 100000
nlines = list([961986,941219,1085676,1179044,1289699,1212277,987245,804125])
files = os.listdir('Citibike Data')
citi_bike_may_dec_2015 = pd.DataFrame()
for i in range(8):
    lines2skip = np.random.choice(np.arange(1,nlines[i]+1), \
    (nlines[i]-nlinesrandomsample), replace=False)
    bike_temp = pd.read_csv('Citibike Data/'+files[i],skiprows = lines2skip)
    citi_bike_may_dec_2015 = citi_bike_may_dec_2015.append(bike_temp)


#Converting to Datetime
citi_bike_may_dec_2015['starttime'] = pd.to_datetime(\
                                            citi_bike_may_dec_2015['starttime'])
citi_bike_may_dec_2015['stoptime'] = pd.to_datetime(\
                                            citi_bike_may_dec_2015['stoptime'])
                                            
citi_bike_may_dec_2015['month'] = pd.DatetimeIndex(citi_bike_may_dec_2015
                                                 ['starttime']).month
citi_bike_may_dec_2015['startdate'] = pd.DatetimeIndex(citi_bike_may_dec_2015
                                                 ['starttime']).date

def cordnts_zip(a,b):
    try:
        location = search.by_coordinate(a,b)
        lctn_zip = location[0]["Zipcode"]
    except:
        lctn_zip = ''
    return lctn_zip

#Removing Incorrect Data
citi_bike_may_dec_2015 = \
citi_bike_may_dec_2015[(citi_bike_may_dec_2015['start station latitude'] != 0 ) & \
(citi_bike_may_dec_2015['start station longitude']!=0 )]  

citi_bike_may_dec_2015 = \
citi_bike_may_dec_2015[(citi_bike_may_dec_2015['end station latitude'] != 0 ) & \
(citi_bike_may_dec_2015['end station longitude']!=0 )]  



citi_bike_may_dec_2015['pickup_zip'] = citi_bike_may_dec_2015.apply(lambda x:\
cordnts_zip(x['start station latitude'],x['start station longitude']),axis=1)   

citi_bike_may_dec_2015['dropoff_zip'] = citi_bike_may_dec_2015.apply(lambda x:\
cordnts_zip(x['end station latitude'],x['end station longitude']),axis=1)



#Removing december data
citi_bike_may_nov_2015 = citi_bike_may_dec_2015[citi_bike_may_dec_2015['month']!= 12]

citi_bike_may_nov_2015.to_csv('citi_bike_may_nov_2015.csv')

           
