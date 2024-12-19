# Importing the required libraries

import streamlit as st
import plotly.express as px
import requests
from geopy.geocoders import Nominatim
import pandas as pd


# MY API KEY FOR WEATHER
api_key = "2c066aa1e14eb8c775dc702d1bcb1ea4"

# Developing the streamlit UI
# st.header("Exploratory Weather Analysis", divider="gray")
# input_city = st.text_input("Enter city/region: ",help='Place to get weather data of.')
# tab1,tab2,tab3 = st.tabs(["Temperature Analysis", "Wind Analysis", "Sky Details"])
# with tab1:
#     input_temp_data = st.segmented_control("Select to see correlation.",options=["Temperature","Pressure","Humidity"]
#                                       ,selection_mode="multi",default=None,help="temp in celsius")
#     heatmap_tab,scatter_tab = st.tabs(["Heatmap","Scatterplot"])
# with tab2:
#     input_wind_data = st.multiselect("Select to see correlation with sky coverage.",options=["Wind Speed","Gust"]
#                                      ,help="Gust is a sudden increase in wind speed above the average wind speed"
#                                      ,default=None)
# with tab3:
#     input_sky_data = st.pills("Please select what to see.",options=["Sunrise","Sunset","Description"],default=None)



geolocator = Nominatim(user_agent="weather_forecast_app")
location = geolocator.geocode("Moscow")
url = (f"http://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}"
       f"&appid={api_key}&units=metric")
content = pd.json_normalize(requests.get(url).json(),record_path=["list"],errors="raise")
number_cols = ['main.temp','main.temp_min', 'main.temp_max', 'main.pressure', 'main.humidity', 'main.temp_kf'
    ,'wind.speed', 'wind.deg', 'wind.gust','dt_txt']
weather_numerical_df = content[number_cols]


sky,description = zip(*[(v[0]["main"],v[0]["description"]) for k,v in content['weather'].items()])
weather_categorical_df = pd.DataFrame(dict(zip(["Sky","Description"],[sky,description])))

parsed_weather_df = pd.concat([weather_numerical_df,weather_categorical_df],axis=1)
print(parsed_weather_df.info())

# Parse the dt_txt into datetime object. Use the datetime as index.

