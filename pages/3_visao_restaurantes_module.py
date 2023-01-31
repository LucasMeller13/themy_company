# Import libraries
import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

# Import dataset
#path = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\train.csv'
df_raw = pd.DataFrame(pd.read_csv('dataset/train.csv'))

# Functions 

def clean_dataset(dataframe):
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
    dataframe['Time_to_deliver'] = (dataframe['Time_taken(min)'].apply(lambda x: str(x).split()[1])).astype(float)
    dataframe['Time_to_deliver'] = dataframe['Time_to_deliver'].apply(lambda x: round(x))
    
    return dataframe


def metric_mean_distance():
    df['distance'] = df[['Restaurant_latitude',
            'Restaurant_longitude',
            'Delivery_location_latitude',
            'Delivery_location_longitude']].apply(lambda x: haversine((x['Restaurant_latitude'],
                                                                        x['Restaurant_longitude']),
                                                                        (x['Delivery_location_latitude'],
                                                                        x['Delivery_location_longitude'])), axis=1)
    mean_distance = round(df.loc[df['distance'] < 80, 'distance'].mean(),2)
    
    return mean_distance


def plot_fig1(): # Tempo médio de entrega por cidade
    mean_city = df.groupby('City')[['Time_to_deliver']].mean().reset_index()
    mean_city['Time_to_deliver'] = mean_city['Time_to_deliver'].apply(lambda x: round(x))
    
    fig1 = px.bar(mean_city, x='Time_to_deliver', y='City', color='City',
                range_x=[mean_city['Time_to_deliver'].min()-5,mean_city['Time_to_deliver'].max()+5])
    
    fig1.update_layout(showlegend=False, hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell", font_color='black'), hoverlabel_align = 'left')
    fig1.update_traces(hovertemplate='<br><b>Cidade:</b> %{y} <br><b>Tempo de entrega:</b> %{x} minutos<extra></extra>')
    
    return fig1
       
        
def plot_fig2(): # Desvio padrão do tempo de entrega por cidade
    std_city = df.groupby('City')[['Time_to_deliver']].std().reset_index()
    std_city['Time_to_deliver'] = std_city['Time_to_deliver'].apply(lambda x: round(x,3))
    
    fig2 = px.bar(std_city, x='Time_to_deliver', y='City', color='City',
                range_x=[std_city['Time_to_deliver'].min()-1,std_city['Time_to_deliver'].max()+1])
    
    fig2.update_layout(showlegend=False, hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell", font_color='black'), hoverlabel_align = 'left')
    fig2.update_traces(hovertemplate='<br><b>Cidade:</b> %{y} <br><b>Desvio padrão:</b> %{x}<extra></extra>')
    
    return fig2
        
        
def plot_fig3(): # Tempo médio de entrega por cidade e por pedido
    mean_city_order = df.groupby(['City','Type_of_order'])[['Time_to_deliver']].mean().reset_index()
    mean_city_order['Time_to_deliver'] = mean_city_order['Time_to_deliver'].apply(lambda x: round(x))
    
    fig3 = px.bar(mean_city_order,
                        x='City',
                        y='Time_to_deliver',
                        color='Type_of_order',
                        text='Type_of_order',
                        range_y=[mean_city_order['Time_to_deliver'].min()-5,mean_city_order['Time_to_deliver'].max()+5],
                        barmode='group')
    
    fig3.update_layout(showlegend=False, hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell", font_color='black'), hoverlabel_align = 'left')
    fig3.update_traces(hovertemplate='<br><b>Tipo de pedido:</b> %{text} <br><b>Cidade:</b> %{x} <br><b>Tempo de entrega:</b> %{y} minutos<extra></extra>')
    
    return fig3
       
        
def plot_fig4(): # Desvio padrão do tempo de entrega por cidade e por pedido
    std_city_order = df.groupby(['City','Type_of_order'])[['Time_to_deliver']].std().reset_index()
    std_city_order['Time_to_deliver'] = std_city_order['Time_to_deliver'].apply(lambda x: round(x,3))
    
    fig4 = px.bar(std_city_order,
                        x='City',
                        y='Time_to_deliver',
                        color='Type_of_order',
                        text='Type_of_order',
                        range_y=[std_city_order['Time_to_deliver'].min()-2,std_city_order['Time_to_deliver'].max()+2],
                        barmode='group')       

    fig4.update_layout(showlegend=False, hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell", font_color='black'), hoverlabel_align = 'left')
    fig4.update_traces(hovertemplate='<br><b>Tipo de pedido:</b> %{text} <br><b>Cidade:</b> %{x} <br><b>Desvio padrão:</b> %{y}<extra></extra>')
    
    return fig4


def plot_fig5(): # Tempo médio de entrega por cidade e por tráfego
    mean_city_road = df.groupby(['City','Road_traffic_density'])[['Time_to_deliver']].mean().reset_index()
    mean_city_road['Time_to_deliver'] = mean_city_road['Time_to_deliver'].apply(lambda x: round(x))
    
    fig5 = px.bar(mean_city_road,
                        x='City',
                        y='Time_to_deliver',
                        color='Road_traffic_density',
                        text='Road_traffic_density',
                        range_y=[mean_city_road['Time_to_deliver'].min()-5,mean_city_road['Time_to_deliver'].max()+5],
                        barmode='group')    
    
    fig5.update_layout(showlegend=False, hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell", font_color='black'), hoverlabel_align = 'left')
    fig5.update_traces(hovertemplate='<br><b>Densidade do tráfego:</b> %{text} <br><b>Cidade:</b> %{x} <br><b>Tempo de entrega:</b> %{y} minutos<extra></extra>')
    
    return fig5


def plot_fig6(): # Desvio padrão do tempo de entrega por cidade e por tráfego
    std_city_road = df.groupby(['City','Road_traffic_density'])[['Time_to_deliver']].std().reset_index()
    std_city_road['Time_to_deliver'] = std_city_road['Time_to_deliver'].apply(lambda x: round(x,3))
    
    fig6 = px.bar(std_city_road,
                    x='City',
                    y='Time_to_deliver',
                    color='Road_traffic_density',
                    text='Road_traffic_density',
                    range_y=[std_city_road['Time_to_deliver'].min()-1,std_city_road['Time_to_deliver'].max()+1],
                    barmode='group')
    
    fig6.update_layout(showlegend=False, hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell", font_color='black'), hoverlabel_align = 'left')
    fig6.update_traces(hovertemplate='<br><b>Densidade do tráfego:</b> %{text} <br><b>Cidade:</b> %{x} <br><b>Desvio padrão:</b> %{y}<extra></extra>')
    
    return fig6


df = clean_dataset(df_raw)

plotly_config = {"displayModeBar": False, "showTips": False}

# ===============
# Visão restaurantes
# ===============

# ========================
#     Layout streamlit
# ========================

# ------- Sidebar -------

st.set_page_config(layout="wide", page_title='Visão Restaurantes', page_icon='🍲')

#image_path = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=150)

st.header('Marketplace - Visão Cliente')

st.markdown('''---''')

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

st.sidebar.markdown('# Powered by Lucas Meller')

df = df[df['Order_Date'] <= data]

# ====================
# ------- Body -------
# ====================

# --------- first container ---------

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        qt_deliver = df['Delivery_person_ID'].nunique()
        st.metric(label='A quantidade de entregadores é de', value=qt_deliver)
        
    with col2:
        st.metric(label='A distância média de entrega é de', value=f'{metric_mean_distance()} km')
    
    with col3:
        mean_time = round(df[df['Festival'] == 'Yes']['Time_to_deliver'].mean())
        st.metric(label='Tempo médio de entrega durante festivais é de', value=f'{mean_time} minutos')
        
    st.markdown('''---''') 
    
# --------- second container ---------

with st.container():
    col4, col5 = st.columns(2)
    
    with col4:
        st.header('Tempo médio de entrega por cidade')
        st.plotly_chart(plot_fig1(), use_container_width=True, config=plotly_config)
        
    with col5:
        st.header('Desvio padrão do tempo de entrega por cidade')
        st.plotly_chart(plot_fig2(), use_container_width=True, config=plotly_config)
    
    st.markdown('''---''')
    
# --------- third container ---------
        
with st.container():
    col6, col7 = st.columns(2)
    
    with col6:
        st.header('Tempo médio de entrega por cidade e por pedido')
        st.plotly_chart(plot_fig3(), use_container_width=True, config=plotly_config)  
        
    with col7:
        st.header('Desvio padrão do tempo de entrega por cidade e por pedido')
        st.plotly_chart(plot_fig4(), use_container_width=True, config=plotly_config)                  
        
    st.markdown('''---''')
    
# --------- fourth container ---------
    
with st.container():
    col8, col9 = st.columns(2)
    
    with col8:
        st.header('Tempo médio de entrega por cidade e por tráfego')
        st.plotly_chart(plot_fig5(), use_container_width=True, config=plotly_config)  
        
    with col9:
        st.header('Desvio padrão do tempo de entrega por cidade e por tráfego')
        st.plotly_chart(plot_fig6(), use_container_width=True, config=plotly_config)  
        
st.markdown('''---''')
        
