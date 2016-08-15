# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 19:46:35 2016

@author: Suhas
"""

#========================= Borough Map

import folium
from folium.element import IFrame
from folium.plugins import MarkerCluster
from IPython.display import HTML, display
import pandas as pd

# Coordinates taken randomly from the NYC data (putting the zoom factor different will give whole New York City view)
NY_COORDINATES = (40.773124694800003, -73.952171325699993)


# definition of the boundaries in the map
district_geo = r'borough.geojson'

# calculating total number of incidents per district
taxi_weather_final2 = pd.DataFrame(taxi_weather_final['Borough_y'].value_counts().astype(float))
taxi_weather_final2.to_json('taxi_weather_final_agg.json')
taxi_weather_final2 = taxi_weather_final2.reset_index()
taxi_weather_final2.columns = ['Borough', 'Number']


# Set threshold values for the color scale on the map
min_val = taxi_weather_final2.Number.min()
q1 = taxi_weather_final2.Number.quantile( .25)
q2 = taxi_weather_final2.Number.quantile( .5)
q3 = taxi_weather_final2.Number.quantile( .75)


# creation of the choropleth
map2 = folium.Map(location = NY_COORDINATES, zoom_start = 10)
map2.choropleth(geo_path = district_geo,
              data_out = 'taxi_weather_final_agg.json',
              data = taxi_weather_final2,
              threshold_scale = [min_val, q1, q2, q3],
              columns = ['Borough', 'Number'],
              key_on = 'feature.properties.borough',
              fill_color = 'YlOrRd',
              fill_opacity = 0.7,
              line_opacity = 0.2,
              legend_name = 'Number of incidents per district')
map2.create_map(path='map3_test.html')

