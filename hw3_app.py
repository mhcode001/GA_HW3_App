#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:50:12 2022

@author: mho
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle 

st.title("Insurance Premium")

url = r"https://raw.githubusercontent.com/mhcode001/GA_HW3_App/main/housing.csv"

num_rows = st.sidebar.number_input('Select Number of Rows to Load', 
                                  min_value =50, 
                                  max_value = 2000, 
                                  step = 50)

section = st.sidebar.radio('Choose Application Section', ['Data Explorer', 
                                                          'Model Explorer'])
print(section)

@st.cache
def load_data(num_rows):
    df = pd.read_csv(url, nrows = num_rows)
    return df

@st.cache
def create_grouping(x_axis, y_axis):
    grouping =  df.groupby(x_axis)[y_axis].mean()
    return grouping

def load_model():
    with open('pipe.pkl', 'rb') as pickled_mod:
        model = pickle.load(pickled_mod)
    return model

df = load_data(num_rows)

if section == 'Data Explorer':
    
    x_axis = st.sidebar.selectbox("Choose column for X-axis",['sex','age','smoker'])
    
    y_axis = st.sidebar.selectbox("Choose column for y-axis",['charges','bmi'])
  
    chart_type = st.sidebar.selectbox("Choose Your Chart Type",
                                       ['line','bar','area'])
    # st.line_chart(grouping)
    
    if chart_type == 'line':
        grouping = create_grouping(x_axis, y_axis)
        st.line_chart(grouping)
        
    elif chart_type == 'bar':
        grouping = create_grouping(x_axis, y_axis)
        st.bar_chart(grouping)
        
    elif chart_type == 'area':
        fig = px.strip(df[[x_axis, y_axis]], x=x_axis, y=y_axis)
        st.plotly_chart(fig)
        
    st.write(df)
    
else:
    st.text("Choose Options to the Side to Explore the Model")
    model = load_model()

    id_val = st.sidebar.selectbox("Choose Restaurant Id",
                                  df['id'].unique().tolist())
    yesterday = st.sidebar.number_input("How many visitors yesterday", min_value = 0,
                                max_value = 100, step =1, value =20)
    day_of_week = st.sidebar.selectbox("Day of Week",
                                df['day_of_week'].unique().tolist())
    
    sample = {
    'id': id_val,
    'yesterday': yesterday,
    'day_of_week': day_of_week
    }


    sample = pd.DataFrame(sample, index = [0])
    prediction = model.predict(sample)[0]
    
    st.title(f"Predicted Attendance: {int(prediction)}")
    
#st.write(df)

#print(num_rows)

