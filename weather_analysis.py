# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:43:45 2016

@author: Suhas
"""
from pandas import Series,  DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.matplotlib.style.use('ggplot')
from itertools import izip_longest
import time
import datetime as datetime
from datetime import *
import dateutil
import statsmodels.formula.api as smf
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
import os 


#======================= Taxi Data ============================
# Loading and cleaning the taxi_dataset
taxi_data = pd.read_csv('nyc_taxi_may_nov_2015.csv',usecols = range(1,25))
# Creating just a date column to merge the weather data
taxi_data['Date'] = pd.to_datetime(taxi_data["tpep_pickup_datetime"]).dt.date


#======================= Weather Data ============================
# Loading and cleaning the weather_dataset
weather_data = pd.read_csv('Weather_Data.csv')#,na_values = 'N.A.', infer_datetime_format=True)
weather_data.columns = weather_data.columns.str.strip()
weather_data['Date'] =  pd.to_datetime(weather_data['Date']).dt.date

# ======================= Final Taxi Dataset =====================
# Creating a final dataset by merging both the taxi data and the weather data
taxi_weather_data = pd.merge(taxi_data, weather_data, on='Date')
taxi_weather_data.columns = taxi_weather_data.columns.str.strip()


# ======================= Weather Analysis =====================
# ======================= Impact of precipitation on the number of rides =====================
unique_events = taxi_weather_data['Events'].unique()

# ======================= Final Taxi Dataset =====================
taxi_dataset_precipitation = taxi_weather_data
taxi_dataset_precipitation = taxi_dataset_precipitation.replace('T', 0)
taxi_dataset_precipitation['PrecipitationIn'] = taxi_dataset_precipitation[['PrecipitationIn']].astype(float)


# ======================= Average number of rides vs Precipitation level =====================
bins = [-0.2 , 0, 0.2, 0.4, 0.6, 3.0]
group_names = ['No','0 - 0.2', '0.2 - 0.4', '0.4 - 0.6', '> 0.6']
categories = pd.cut(taxi_dataset_precipitation['PrecipitationIn'], bins, labels=group_names)
taxi_dataset_precipitation['categories'] = pd.cut(taxi_dataset_precipitation['PrecipitationIn'], bins, labels=group_names)
taxi_dataset_precipitation['Date'] = pd.to_datetime(taxi_dataset_precipitation['Date'])
taxi_dataset_precipitation = taxi_dataset_precipitation[taxi_dataset_precipitation['Date']< pd.to_datetime('2015-12-01')]

x = taxi_dataset_precipitation.groupby(['categories']).size()
y = np.transpose(taxi_dataset_precipitation.groupby(['categories','Date']).size().unstack())
precipitation = []
precipitation.append(x[0]/y['No'].count())
precipitation.append(x[1]/y['0 - 0.2'].count())
precipitation.append(x[2]/y['0.2 - 0.4'].count())
precipitation.append(x[3]/y['0.4 - 0.6'].count())
precipitation.append(x[4]/y['> 0.6'].count())

#======================== Precipitation's effect on the number of rides for Yellow Taxis ============
precipitation = pd.Series(precipitation,index = ['No','0 - 0.2','0.2 - 0.4','0.4 - 0.6','> 0.6'])
precipitation.plot(kind='bar')
plt.xlabel('Precipitation in inches')
plt.ylabel('Average Daily Trips')
plt.title('Precipitation vs NYC Taxi Trips')
plt.show()

#======================== ANOVA analysis ========================
# To check if the mean of rides are different for different level of precipitation
t1 = taxi_dataset_precipitation[taxi_dataset_precipitation['categories'] == 'No']['Date']
t2 = DataFrame(t1, columns = ['Date'])
t3 = t2.groupby(['Date']).size()

t4 = taxi_dataset_precipitation[taxi_dataset_precipitation['categories'] == '0 - 0.2']['Date']
t5 = DataFrame(t4, columns = ['Date'])
t6 = t5.groupby(['Date']).size()

t7 = taxi_dataset_precipitation[taxi_dataset_precipitation['categories'] == '0.2 - 0.4']['Date']
t8 = DataFrame(t7, columns = ['Date'])
t9 = t8.groupby(['Date']).size()

t10 = taxi_dataset_precipitation[taxi_dataset_precipitation['categories'] == '0.4 - 0.6']['Date']
t11 = DataFrame(t10, columns = ['Date'])
t12 = t11.groupby(['Date']).size()

t13 = taxi_dataset_precipitation[taxi_dataset_precipitation['categories'] == '> 0.6']['Date']
t14 = DataFrame(t13, columns = ['Date'])
t15 = t14.groupby(['Date']).size()

tfinal = DataFrame({'a':t3, 'b':t6, 'c':t9, 'd':t12, 'e':t15})
tfinal.fillna(tfinal.mean())

t16 = DataFrame(t3, columns = ['No'])
t17 = DataFrame(t6, columns = ['0 - 0.2'])
t18 = DataFrame(t9, columns = ['0.2 - 0.4'])
t19 = DataFrame(t12, columns = ['0.4 - 0.6'])
t20 = DataFrame(t15, columns = ['> 0.6'])


#======================== ANOVA test
from scipy import stats
    f_val, p_val = stats.f_oneway(t3, t6, t9, t12, t15)

print ('\n')
print ('We observe the p-value to be {:.2f}').format(p_val)
print ('Thus, we can accept Ho and conclude that the average rides irrespective of the precipitation are same')

#================== Box plot showing the variation in number of rides based on precipitation ======================
    data_to_plot = [t3, t6, t9, t12, t15]
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_to_plot)
    ax.set_xticklabels(['No', '0 - 0.2', '0.2 - 0.4', '0.4 - 0.6', '> 0.6'])
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()











