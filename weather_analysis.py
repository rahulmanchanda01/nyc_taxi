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
taxi_data = pd.read_csv('nyc_taxi_may_dec2015_newfile.csv',usecols = range(1,25))#,na_values = 'N.A.', parse_dates = ['tpep_pickup_datetime'], infer_datetime_format=True)
#taxi_data = taxi_data.drop('Unnamed: 0', 1)
# Creating just a date column to merge the weather data
taxi_data['Date'] = pd.to_datetime(taxi_data["tpep_pickup_datetime"]).dt.date


#======================= Weather Data ============================
# Loading and cleaning the weather_dataset
weather_data = pd.read_csv('Weather_Data.csv')#,na_values = 'N.A.', infer_datetime_format=True)
weather_data.columns = weather_data.columns.str.strip()
weather_data['Date'] =  pd.to_datetime(weather_data['Date'])

testweather = weather_data[(weather_data['Date'] < datetime.strptime('20151201','%Y%m%d')) & (weather_data['Date'] > datetime.strptime('20150430','%Y%m%d'))]
# Converting date column to datetime, easier to merge
#weather_data['Date'] = pd.to_datetime(weather_data["Date"])
#weather_data['Date'] = [d.date() for d in weather_data["Date"]]


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

precipitation = pd.Series(precipitation,index = ['No','0 - 0.2','0.2 - 0.4','0.4 - 0.6','> 0.6'])
precipitation.plot(kind='bar')
plt.xlabel('Precipitation in inches')
plt.ylabel('Average Daily Trips')
plt.title('Precipitation vs NYC Taxi Trips')
plt.show()



