# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 15:14:58 2016

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
import dateutil
import statsmodels.formula.api as smf
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
import os 

#======================= Taxi Data ============================
# Loading and cleaning the taxi_dataset
taxi_data = pd.read_csv('nyc_taxi_may_dec2015.csv',na_values = 'N.A.', parse_dates = ['tpep_pickup_datetime'], infer_datetime_format=True)
taxi_data = taxi_data.drop('Unnamed: 0.1', 1)
taxi_data = taxi_data.drop('Unnamed: 0', 1)
# Creating just a date column to merge the weather data
taxi_data['Date'] = [d.date() for d in taxi_data["tpep_pickup_datetime"]]

#======================= Weather Data ============================
# Loading and cleaning the weather_dataset
weather_data = pd.read_csv('Weather_Data.csv',na_values = 'N.A.', infer_datetime_format=True)
weather_data['Date'] =  pd.to_datetime(weather_data['Date'])
# Converting date column to datetime, easier to merge
weather_data['Date'] = [d.date() for d in weather_data["Date"]]

#======================= NYC Borough Data ============================
# Loading and cleaning the Borough Data
borough_data = pd.read_csv('borough_data.csv')


# ======================= Final Taxi Dataset =====================
# Creating a final dataset by merging both the taxi data and the weather data
taxi_weather = pd.merge(taxi_data, weather_data, left_on='Date', right_on='Date', how = 'left')

# Creating a pickup borough
taxi_weather_pickup = pd.merge(taxi_weather, borough_data, left_on='pickup_zip', right_on='Zipcode', how = 'left')

# Creating a dropoff borough
taxi_weather_final = pd.merge(taxi_weather_pickup, borough_data, left_on='dropoff_zip', right_on='Zipcode', how = 'left')



#================================= Plotting Clustered pickups

import folium
from folium.element import IFrame
from folium.plugins import MarkerCluster
from IPython.display import HTML, display
import pandas as pd

# Coordinates taken randomly from the NYC data (putting the zoom factor different will give whole New York City view)
NY_COORDINATES = (40.773124694800003, -73.952171325699993)

# As of now taking just 1000 records. Can be implemented for overall data
MAX_RECORDS = 1000

# create empty map zoomed in on San Francisco
map_1 = folium.Map(location=NY_COORDINATES, zoom_start = 10)

# create a marker cluster called "Pickups"
marker_cluster_1 = folium.MarkerCluster("Pickups").add_to(map_1)

# add a marker for every record in the filtered data, use a clustered view
for each in taxi_weather_final[0:MAX_RECORDS].iterrows():
    folium.Marker([each[1]['pickup_latitude'],each[1]['pickup_longitude']]).add_to(marker_cluster_1)
map_1.create_map(path='map_1.html')
