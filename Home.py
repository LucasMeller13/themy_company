import datetime

import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title='Home', page_icon='📃')

#image_path = 'C:\\Users\\lucas\\OneDrive\\CDS\\jupyter\\logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=150)

st.header('Marketplace')

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

st.sidebar.markdown('# Powered by Lucas Meller')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - **Visão Empresa:** 
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - **Visão Entregador:** 
        - Acompanhamento dos indicadores semanais de crescimento
    - **Visão Restaurante:**
        - Indicadores semanais de crescimento dos restaurantes
""" )
