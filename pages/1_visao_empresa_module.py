# Import libraries
import datetime

import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

# Import dataset
#path_df_raw = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\train.csv'
df_raw = pd.DataFrame(pd.read_csv('dataset\\train.csv'))

# Functions

def clean_dataframe(dataframe):
    dataframe['ID'] = dataframe['ID'].str.strip()
    dataframe['Delivery_person_ID'] = dataframe['Delivery_person_ID'].str.strip()
    dataframe['Road_traffic_density'] = dataframe['Road_traffic_density'].str.strip()
    dataframe['Type_of_order'] = dataframe['Type_of_order'].str.strip()
    dataframe['Type_of_vehicle'] = dataframe['Type_of_vehicle'].str.strip()
    dataframe['Festival'] = dataframe['Festival'].str.strip()
    dataframe['City'] = dataframe['City'].str.strip()
    dataframe['multiple_deliveries'] = dataframe['multiple_deliveries'].astype(float)
    dataframe = dataframe[dataframe.isin(['NaN']) != True]
    dataframe = dataframe[dataframe.isin(['NaN ']) != True]
    dataframe = dataframe[dataframe['Weatherconditions'] != 'conditions NaN']
    dataframe['Order_Date'] = pd.to_datetime(dataframe['Order_Date'], format='%d-%m-%Y')

    return dataframe


def plot_fig1():
    x = df.groupby(['Order_Date'])[['ID']].count().reset_index().sort_values(by='Order_Date')
    fig1 = px.bar(data_frame=x, x='Order_Date', y='ID')
    
    return fig1


def plot_fig2():
    df['week_of_the_year'] = df['Order_Date'].dt.strftime('%W')
    df_pizza = df.groupby('Road_traffic_density')[['ID']].count().reset_index()
    fig2 = px.pie(names=list(df_pizza['Road_traffic_density']), values=list(df_pizza['ID']))
    fig2.update_traces(textinfo='percent+label', textposition='inside', hoverinfo='label+percent', marker=dict(line=dict(color='#000000', width=1)))
    
    return fig2


def plot_fig3():
    df_multiple_index = df.groupby(['City','Road_traffic_density'])[['ID']].count().reset_index()
    fig3 = px.bar(df_multiple_index, x='City', y='ID', color='Road_traffic_density', barmode='group', text='Road_traffic_density')
    
    return fig3


def plot_fig4():
    x = df.groupby(['Order_Date'])[['ID']].count().reset_index().sort_values(by='Order_Date')
    x['week_of_the_year'] = x['Order_Date'].dt.strftime('%W')
    y = x.groupby('week_of_the_year')[['ID']].sum().reset_index()
    fig4 = px.line(data_frame=y, x='week_of_the_year', y='ID')
    
    return fig4    


def plot_fig5():
    fig5 = df.groupby(['week_of_the_year'])[['ID']].count().reset_index().sort_values(by='week_of_the_year')
    figy = df.groupby(['week_of_the_year'])[['Delivery_person_ID']].nunique().reset_index().sort_values(by='week_of_the_year')
    fig5['result'] = fig5['ID'] / figy['Delivery_person_ID']
    fig5['week_of_the_year'] = fig5['week_of_the_year'].astype(float)
    fig5 = fig5.sort_values(by='week_of_the_year')
    
    return fig5


def plot_fig6():
    fig6 = df.groupby(['City','Road_traffic_density'])[['Restaurant_latitude','Restaurant_longitude']].median().reset_index()
    map = folium.Map()
    
    for i in range(len(fig6)):
        folium.Marker([fig6.loc[i, 'Restaurant_latitude'], fig6.loc[i, 'Restaurant_longitude']]).add_to(map)
        
    return map 

df = clean_dataframe(df_raw)

# ===============
# Visão empresa
# ===============

# ========================
#     Layout streamlit
# ========================

# ------- Sidebar -------
st.set_page_config(layout="wide", page_title='Visão Empresa', page_icon='📈')

#image_path = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=150)

st.header('Marketplace - Visão Cliente')

st.sidebar.markdown('# Themy Company')
st.sidebar.markdown('## Fastest delivery in town')
st.sidebar.markdown('''---''')

st.sidebar.markdown('# Selecione uma data limite')
data = (st.sidebar.slider('Até qual valor?',
                        min_value=datetime.datetime(2022,2,11),
                        max_value=datetime.datetime(2022,4,6),
                        value=datetime.datetime(2022,3,19),
                        format='DD-MM-YYYY'))

st.sidebar.markdown('''---''')

options = st.sidebar.multiselect(label='Escolha um tipo de tráfego:',
                                 options=['High', 'Jam', 'Low', 'Medium'],
                                 default='High')

st.sidebar.markdown('''---''')

st.sidebar.markdown('# Powered by Meller')

# ===================================

df = df[(df['Order_Date'] <= data) & (df['Road_traffic_density'].isin(options))]

# ------- Template -------

tab1,tab2,tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    
    with st.container():   
        st.header('Orders by Day')
        st.plotly_chart(plot_fig1(), use_container_width=True)
    
    col1,col2 = st.columns(2)
    
    with st.container():
        
        with col1: 
            st.header('Traffic Order Share')
            st.plotly_chart(plot_fig2(), use_container_width=True)
            
        with col2:
            st.header('Traffic Order City')
            st.plotly_chart(plot_fig3(), use_container_width=True)
        
with tab2:
    
    with st.container():
        st.header('Delivery per Week')
        st.plotly_chart(plot_fig4(), use_container_width=True)
        
    st.markdown('''---''')
    
    with st.container():
        st.header('Delivery Mean per Week per Delivery Person')
        st.plotly_chart(px.line(plot_fig5(), x='week_of_the_year', y='result'), use_container_width=True)
        
with tab3:
    st.header('Country Maps')
    folium_static(plot_fig6(), width=1024, height=600)