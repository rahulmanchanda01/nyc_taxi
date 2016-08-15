# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 19:51:40 2016

@author: Suhas
"""


#=========================== Heat Map

import folium
from folium import plugins
stops_heatmap = folium.Map(location= NY_COORDINATES , zoom_start = 10)
stops_heatmap.add_children(plugins.HeatMap([[row['dropoff_latitude'], row['dropoff_longitude']] for name, row in taxi_weather_final.iterrows()]))
stops_heatmap.save("heatmap_dropoff.html")
