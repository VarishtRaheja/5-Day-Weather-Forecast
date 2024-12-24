# Importing the required libraries

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# MY API KEY FOR WEATHER
api_key = "2c066aa1e14eb8c775dc702d1bcb1ea4"

# Developing the streamlit UI
st.header("Exploratory Weather Analysis", divider="gray")
input_city = st.text_input("Enter city/region: ",help='Place to get weather data of.').capitalize()

if input_city:
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={input_city}&appid={api_key}&units=metric"
    content = pd.json_normalize(requests.get(url).json(), record_path=["list"], errors="raise")
    number_cols = ['main.temp', 'main.temp_min', 'main.temp_max', 'main.pressure', 'main.humidity', 'main.temp_kf'
        , 'wind.speed', 'wind.deg', 'wind.gust', 'dt_txt']
    weather_numerical_df = content[number_cols]
    sky, description = zip(*[(v[0]["main"], v[0]["description"]) for k, v in content['weather'].items()])
    weather_categorical_df = pd.DataFrame(dict(zip(["Sky", "Description"], [sky, description])))

    # Parse the dt_txt into datetime object. Use the datetime as index.
    weather_numerical_df['dt_txt'] = pd.to_datetime(weather_numerical_df['dt_txt'], utc=True
                                                    , format="%Y-%m-%d %H:%M:%S")

    # Exploratory data analysis
    tabs = ["Heatmap", "Scatterplot", "Lineplot","Sky Conditions"]
    layouts = st.pills("Plots",options=tabs,selection_mode="single")

    if layouts=="Heatmap":
        st.subheader('Inter-correlation Matrix Heatmap')
        with sns.axes_style("darkgrid"):
            fig,ax = plt.subplots(figsize=(10,6))
            ax = sns.heatmap(weather_numerical_df.corr(),vmax=1,square=True,annot=True,fmt=".1f",linewidths=0.5,cmap="crest")
        st.pyplot(fig)
        plt.clf()

    if layouts == "Scatterplot":
        option_map = {0: "main.pressure",1: "main.humidity",2: "wind.speed"}
        selection = st.segmented_control("Correlation between",options=option_map.keys(), format_func=lambda option: option_map[option],
            selection_mode="single", default=0
        )
        with sns.axes_style("darkgrid"):
            st.subheader(f"Correlation between {option_map[selection]} and Temperature")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax = sns.regplot(weather_numerical_df, x="main.temp", y=f"{option_map[selection]}", fit_reg=True, color="red", marker="o")
        st.pyplot(fig)
        plt.clf()

    if layouts == "Lineplot":

        option_map = {0: "main.pressure", 1: "main.humidity", 2: "wind.speed",3:"main.temp"}
        # forecast_days = st.slider("Forecast Days", min_value=1, max_value=5, step=1,
                                  # help="Move the slider to select a day.")
        sel_drop = st.selectbox("Variation",options=option_map.keys()
                                ,format_func=lambda option: option_map[option]
                                ,help="Will show line plot on choice")
        fig = px.line(data_frame=weather_numerical_df,x="dt_txt",y=f"{option_map[sel_drop]}",markers=True)
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    if layouts == "Sky Conditions":
        fig = px.bar(data_frame=weather_categorical_df,x="Description")
        st.plotly_chart(fig,theme="streamlit")