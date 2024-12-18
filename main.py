# Importing the required libraries

import streamlit as st
import plotly.express as px
import requests
from geopy.geocoders import Nominatim
import pandas as pd

# Basic UI for forecast.
st.title('Weather Forecast Dashboard')
city_name = st.text_input("Please enter place/city name:").capitalize()
forecast_days = st.slider("Forecast Days",min_value=1,max_value=5,step=1,help="Move the slider to select a day.")
drop_down_option = st.selectbox("Select data to view",options=["Temperature","Sky"],help="The data will be displayed below this.")
st.subheader(f"{drop_down_option} data for {forecast_days} day(s) in {city_name}.",help="Explanation",divider=True)


# MY API KEY FOR WEATHER
api_key = "2c066aa1e14eb8c775dc702d1bcb1ea4"

# Getting data from url.
def get_data_url(place,days):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="weather_forecast_app")
    location = geolocator.geocode(place)
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    content = response["list"][:8*days] # This is filtered depending on 5 days data for 24 hours.
    return response, content


if city_name:
    weather_df, filtered_data = get_data_url(place=city_name,days=forecast_days)
    if drop_down_option == "Temperature":
        data = [data["dt_txt"] for data in filtered_data]
        dates = pd.to_datetime(data, utc=True)
        filtered_data_temperature = [temp_data["main"]["temp"] for temp_data in filtered_data]
        temperature_dataframe = pd.DataFrame(data=zip(dates,filtered_data_temperature),columns=["Date","Temperature"])
        # Plotting temp data.

        fig = px.line(x=temperature_dataframe["Date"],y=temperature_dataframe["Temperature"]
                      ,labels={"x":"Dates","y":"Temperature(C)"},title='Temperature based on forecasted days.',markers=True)
        st.plotly_chart(fig,theme='streamlit',use_container_width=True,on_select='rerun')

    if drop_down_option == "Sky":
        # Plotting sky conditions
        filtered_data_sky = [temp_data["weather"][0]["main"] for temp_data in filtered_data]
        images_dict = {"Clouds":"images/cloud.png","Clear":"images/clear.png","Rain":"images/rain.png","Snow":"images/snow.png"}
        images = [images_dict[conditions] for conditions in filtered_data_sky]
        st.image(images,width=120)




