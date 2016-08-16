# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 13:22:53 2016

@author: SuryaNarayana
"""
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import plotly.plotly as py
py.sign_in('suryak1210', 'nd72ait1tg')
import folium 
from folium.element import IFrame
from folium.plugins import MarkerCluster
from folium import plugins
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


nyc_taxi_may_dec2015 =  pd.read_csv('nyc_taxi_may_dec2015.csv')
bike_may_dec_2015 = pd.read_csv('bike_may_dec_2015.csv')
nyc_taxi_may_dec2015['Time'] = pd.to_datetime(nyc_taxi_may_dec2015['Time'])
nyc_taxi_may_dec2015['tpep_pickup_datetime'] = pd.to_datetime(nyc_taxi_may_dec2015['tpep_pickup_datetime'])
nyc_taxi_may_dec2015['tpep_dropoff_datetime'] = pd.to_datetime(nyc_taxi_may_dec2015['tpep_dropoff_datetime'])

########################Basic plot done##############################
##########################################################################

#################### nyc_taxi_may_dec2015 pickup ###################################
NY_COORDINATES = (40.773124694800003, -73.952171325699993)

# for speed purposes
MAX_RECORDS = 1000
 

# create empty map zoomed in on New York
nyc_taxi_may_dec2015_pickup = folium.Map(location=NY_COORDINATES, zoom_start=12)

marker_cluster = folium.MarkerCluster("Pickups").add_to(nyc_taxi_may_dec2015_pickup)
#add a marker for every record in the filtered data, use a clustered view
for each in nyc_taxi_may_dec2015[0:MAX_RECORDS].iterrows():
     folium.Marker([each[1]['pickup_latitude'],each[1]['pickup_longitude']])\
     .add_to(marker_cluster)

nyc_taxi_may_dec2015_pickup.create_map(path = 'nyc_taxi_may_dec2015_pickup.html')
#folium.TileLayer('nyc_taxi_may_dec2015_pickup').add_to(nyc_taxi_may_dec2015_pickup)
#folium.LayerControl().add_to(nyc_taxi_may_dec2015_pickup)

#################### nyc_taxi_may_dec2015 dropff ###################################
# create empty map zoomed in on New York
nyc_taxi_may_dec2015_dropff = folium.Map(location=NY_COORDINATES, zoom_start=12)

marker_cluster = folium.MarkerCluster("Dropoff").add_to(nyc_taxi_may_dec2015_dropff)
#add a marker for every record in the filtered data, use a clustered view

#add a marker for every record in the filtered data, use a clustered view
for each in nyc_taxi_may_dec2015[0:MAX_RECORDS].iterrows():
     folium.Marker([each[1]['dropoff_latitude'],each[1]['dropoff_longitude']])\
     .add_to(marker_cluster)
nyc_taxi_may_dec2015_dropff.create_map(path = 'nyc_taxi_may_dec2015_dropff.html')
#folium.TileLayer('nyc_taxi_may_dec2015_dropff').add_to(nyc_taxi_may_dec2015_pickup)

##################### bike_may_dec_2015 start ######################################

# create empty map zoomed in on New York
bike_may_dec_2015_start = folium.Map(location=NY_COORDINATES, zoom_start=12)

marker_cluster = folium.MarkerCluster("start").add_to(bike_may_dec_2015_start)
#add a marker for every record in the filtered data, use a clustered view

#add a marker for every record in the filtered data, use a clustered view
for each in bike_may_dec_2015[0:MAX_RECORDS].iterrows():
     folium.Marker([each[1]['start station latitude'],each[1]['start station longitude']])\
     .add_to(marker_cluster)
bike_may_dec_2015_start.create_map(path = 'bike_may_dec_2015_start.html')
#folium.TileLayer('bike_may_dec_2015_start').add_to(nyc_taxi_may_dec2015_pickup)

##################### bike_may_dec_2015 end ######################################

# create empty map zoomed in on New York
bike_may_dec_2015_end = folium.Map(location=NY_COORDINATES, zoom_start=12)

marker_cluster = folium.MarkerCluster("end").add_to(bike_may_dec_2015_end)
#add a marker for every record in the filtered data, use a clustered view

#add a marker for every record in the filtered data, use a clustered view
for each in bike_may_dec_2015[0:MAX_RECORDS].iterrows():
     folium.Marker([each[1]['end station latitude'],each[1]['end station longitude']])\
     .add_to(marker_cluster)
bike_may_dec_2015_end.create_map(path = 'bike_may_dec_2015_end.html')
#folium.TileLayer('bike_may_dec_2015_end').add_to(nyc_taxi_may_dec2015_pickup)

###########################################################################

nyc_taxi_may_dec2015_latenight = nyc_taxi_may_dec2015[nyc_taxi_may_dec2015['Time'] > '23:30:00' ]

stops_heatmap = folium.Map(location= NY_COORDINATES , zoom_start = 12)
stops_heatmap.add_children(plugins.HeatMap([[row['pickup_latitude'],\
row['pickup_longitude']] for name, row in nyc_taxi_may_dec2015_latenight.iterrows()]))
stops_heatmap.save("nyc_taxi_may_dec2015_latenight.html")
#stops_heatmap


####################### weekday vs weekend heatmap###################################################

nyc_taxi_may_dec2015_weekday = nyc_taxi_may_dec2015[nyc_taxi_may_dec2015['tpep_pickup_datetime'].str.contains('2015-10-12')]

stops_heatmap = folium.Map(location= NY_COORDINATES , zoom_start = 12)
stops_heatmap.add_children(plugins.HeatMap([[row['pickup_latitude'],\
row['pickup_longitude']] for name, row in nyc_taxi_may_dec2015_weekday.iterrows()]))
stops_heatmap.save("nyc_taxi_may_dec2015_weekday.html")
#stops_heatmap

nyc_taxi_may_dec2015_weekend = nyc_taxi_may_dec2015[nyc_taxi_may_dec2015['tpep_pickup_datetime'].str.contains('2015-10-11')]

stops_heatmap = folium.Map(location= NY_COORDINATES , zoom_start = 12)
stops_heatmap.add_children(plugins.HeatMap([[row['pickup_latitude'],\
row['pickup_longitude']] for name, row in nyc_taxi_may_dec2015_weekend.iterrows()]))
stops_heatmap.save("nyc_taxi_may_dec2015_weekend.html")
#stops_heatmap



###################### Peak hour vs non peak hour##############################

nyc_hourly = nyc_taxi_may_dec2015['pickup_time'].sum()

nyc_taxi_may_dec2015.hist(nyc_taxi_may_dec2015['Time'],nyc_taxi_may_dec2015['Time'].count())
plt.show()

nyc_taxi_may_dec2015_peak = nyc_taxi_may_dec2015[(nyc_taxi_may_dec2015['tpep_pickup_datetime'] < pd.to_datetime('09:00:00')) &
                (nyc_taxi_may_dec2015['tpep_pickup_datetime']> pd.to_datetime('08:00:00'))] 

nyc_taxi_may_dec2015_nonpeak = nyc_taxi_may_dec2015[(nyc_taxi_may_dec2015['tpep_pickup_datetime'] < pd.to_datetime('23:59:00')) &
                (nyc_taxi_may_dec2015['tpep_pickup_datetime']> pd.to_datetime('23:00:00'))] 

stops_heatmap = folium.Map(location= NY_COORDINATES , zoom_start = 12)
stops_heatmap.add_children(plugins.HeatMap([[row['pickup_latitude'],\
row['pickup_longitude']] for name, row in nyc_taxi_may_dec2015_peak.iterrows()]))
stops_heatmap.save("nyc_taxi_may_dec2015_peak.html")
#stops_heatmap

stops_heatmap = folium.Map(location= NY_COORDINATES , zoom_start = 12)
stops_heatmap.add_children(plugins.HeatMap([[row['pickup_latitude'],\
row['pickup_longitude']] for name, row in nyc_taxi_may_dec2015_nonpeak.iterrows()]))
stops_heatmap.save("nyc_taxi_may_dec2015_nonpeak.html")
#stops_heatmap


##########################################################################
geo_path = r'zip.geojson'

# Set threshold values for the color scale on the map
min_val = nyc_taxi_may_dec2015_oct.number_of_searches.min()
q1 = nyc_taxi_may_dec2015_oct.number_of_searches.quantile( .25)
q2 = nyc_taxi_may_dec2015_oct.number_of_searches.quantile( .5)
q3 = nyc_taxi_may_dec2015_oct.number_of_searches.quantile( .75)

# Create map object and bind our data to it
map = folium.Map(location=[37.769959, -122.448679], zoom_start=9)
map.geo_json(geo_path=geo_path, data=nyc_taxi_may_dec2015_oct, data_out = 'nyc_taxi_may_dec2015_oct.json',
             columns=['ZCTA5CE10', 'number_of_searches'],
             threshold_scale=[min_val, q1, q2, q3],
             key_on='feature.properties.ZCTA5CE10',
             fill_color='BuPu', fill_opacity=0.9, line_opacity=0.9,
             legend_name='Number of Searches')

map.create_map(path='sfmetro_number_of_searches.html')