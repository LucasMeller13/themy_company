# Import libraries
import datetime

import folium
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

# Import dataset
#path_df = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\train.csv'
df_raw = pd.DataFrame(pd.read_csv('dataset/train.csv'))

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
    dataframe['Delivery_person_Age'] = dataframe['Delivery_person_Age'].astype(float)
    dataframe['Delivery_person_Ratings'] = dataframe['Delivery_person_Ratings'].astype(float)
    dataframe = dataframe.reset_index(drop=True)

    return dataframe


def plot_fig1():    
    df['Time_to_deliver'] = (df['Time_taken(min)'].apply(lambda x: str(x).split()[1])).astype(float)
    xx = df[['Delivery_person_ID','Time_to_deliver']].groupby('Delivery_person_ID')[['Time_to_deliver']].mean().sort_values('Time_to_deliver').reset_index().head(10)
    fig1 = px.bar(xx, x='Time_to_deliver',
                y='Delivery_person_ID',
                range_x=[xx['Time_to_deliver'].min()-0.06,xx['Time_to_deliver'].max()+0.06],
                labels={'Time_to_deliver':'tempo_entrega', 'Delivery_person_ID':'id_entregador'},
                color='Delivery_person_ID')
    fig1.update_traces(showlegend=False) 
    
    return fig1


def plot_fig2():
    df['Time_to_deliver'] = (df['Time_taken(min)'].apply(lambda x: str(x).split()[1])).astype(float)
    yy = df[['Delivery_person_ID','Time_to_deliver']].groupby('Delivery_person_ID')[['Time_to_deliver']].mean().sort_values('Time_to_deliver', ascending=False).reset_index().head(10)
    fig2 = px.bar(yy, x='Time_to_deliver',
                y='Delivery_person_ID',
                range_x=[yy['Time_to_deliver'].min()-0.06,yy['Time_to_deliver'].max()+0.06],
                labels={'Time_to_deliver':'tempo_entrega', 'Delivery_person_ID':'id_entregador'},
                color='Delivery_person_ID')
    fig2.update_traces(showlegend=False)
    
    return fig2


def plot_fig3():
    mean_density = df.groupby('Road_traffic_density')[['Delivery_person_Ratings']].mean().reset_index()
    fig3 = px.bar(mean_density, x='Delivery_person_Ratings', y='Road_traffic_density',
                range_x=[mean_density['Delivery_person_Ratings'].min()-0.01, mean_density['Delivery_person_Ratings'].max()+0.01],
                labels={'Delivery_person_Ratings':'avaliacao_entregador','Road_traffic_density':'densidade_transito'},
                color='Road_traffic_density')
    fig3.update_traces(showlegend=False)
    
    return fig3


def plot_fig4():
    std_density = df.groupby('Road_traffic_density')[['Delivery_person_Ratings']].std().reset_index()
    fig4 = px.bar(std_density, x='Delivery_person_Ratings', y='Road_traffic_density',
                range_x=[std_density['Delivery_person_Ratings'].min()-0.01, std_density['Delivery_person_Ratings'].max()+0.01],
                labels={'Delivery_person_Ratings':'avaliacao_entregador','Road_traffic_density':'densidade_transito'},
                color='Road_traffic_density')
    fig4.update_traces(showlegend=False)
    
    return fig4


def plot_fig5():    
    mean_weather = df.groupby('Weatherconditions')[['Delivery_person_Ratings']].mean().reset_index()
    fig5 = px.bar(mean_weather, x='Delivery_person_Ratings', y='Weatherconditions',
                range_x=[mean_weather['Delivery_person_Ratings'].min()-0.02,mean_weather['Delivery_person_Ratings'].max()+0.02],
                labels={'Delivery_person_Ratings':'avaliacao_entregador','Weatherconditions':'condicao_climatica'},
                color='Weatherconditions')
    fig5.update_traces(showlegend=False)
    
    return fig5


def plot_fig6():
    std_weather = df.groupby('Weatherconditions')[['Delivery_person_Ratings']].std().reset_index()
    fig6 = px.bar(std_weather, x='Delivery_person_Ratings', y='Weatherconditions',
                range_x=[std_weather['Delivery_person_Ratings'].min()-0.02,std_weather['Delivery_person_Ratings'].max()+0.02],
                labels={'Delivery_person_Ratings':'avaliacao_entregador','Weatherconditions':'condicao_climatica'},
                color='Weatherconditions')
    fig6.update_traces(showlegend=False)
    
    return fig6


df = clean_dataframe(df_raw)

# ===============
# Visão entregadores
# ===============

# ========================
#     Layout streamlit
# ========================

# ------- Sidebar -------
st.set_page_config(layout="wide", page_title='Visão Entregadores', page_icon='🚲')

#image_path = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=150)

st.header('Marketplace - Visão Entregadores')

st.markdown('''---''')

st.sidebar.markdown('# Themy Company')
st.sidebar.markdown('## Fastest delivery in town')

st.sidebar.markdown('''---''')

st.sidebar.markdown('# Selecione uma data limite')
data = (st.sidebar.slider('Até qual data?',
                        min_value=datetime.datetime(2022,2,11),
                        max_value=datetime.datetime(2022,4,6),
                        value=datetime.datetime(2022,3,19),
                        format='DD-MM-YYYY'))

st.sidebar.markdown('''---''')

df = df[df['Order_Date'] <= data]

# --------- Body ---------

col1, col2, col3, col4 = st.columns(4)

with st.container():
    with col1:
        max_age = int(df['Delivery_person_Age'].max())
        st.metric(label='O entregador mais velho possui', value=f'{max_age} anos')

    with col2:
        min_age = int(df['Delivery_person_Age'].min())
        st.metric(label='O entregador mais novo possui', value=f'{min_age} anos')
    
    with col3:
        max_vCondition = df['Vehicle_condition'].max()
        st.metric(label='A melhor condição do veículo é de', value=f'{max_vCondition}')
    
    with col4:    
        min_vCondition = df['Vehicle_condition'].min()
        st.metric(label='A pior condição do veículo é de', value=f'{min_vCondition}')
    
    st.markdown('''---''')

with st.container():
    col5, col6 = st.columns(2)
    
    with col5:   
        st.header('Top 10 entregadores mais rápidos')
        st.plotly_chart(plot_fig1(), use_container_width=True, config={"displayModeBar": False, "showTips": False})
    
    with col6:
        st.header('Top 10 entregadores mais lentos')
        st.plotly_chart(plot_fig2(), use_container_width=True, config={"displayModeBar": False, "showTips": False})
    
    st.markdown('''---''')

with st.container():
    col7, col8, col9 = st.columns(3)
    
    with col7:
        w = df.groupby('Delivery_person_ID')[['Delivery_person_Ratings']].mean().reset_index()
        st.markdown('### Avaliação média por entregador')
        st.dataframe(w, width=350)

    with col8: 
        st.markdown('### Avaliação média por tipo de tráfego')
        st.plotly_chart(plot_fig3(), use_container_width=True, config={"displayModeBar": False, "showTips": False})
        
    with col9:
        st.markdown('### Avaliação desvio padrão por tipo de tráfego')
        st.plotly_chart(plot_fig4(), use_container_width=True, config={"displayModeBar": False, "showTips": False})
    
    st.markdown('''---''')
        
with st.container():
    col10, col11 = st.columns(2)
    
    with col10:
        st.markdown('### Avaliação média por condição climática')
        st.plotly_chart(plot_fig5(), use_container_width=True, config={"displayModeBar": False, "showTips": False})
        
    with col11:
        st.markdown('### Avaliação desvio padrão por condição climática')
        st.plotly_chart(plot_fig6(), use_container_width=True, config={"displayModeBar": False, "showTips": False})
    
    st.markdown('''---''')
        
