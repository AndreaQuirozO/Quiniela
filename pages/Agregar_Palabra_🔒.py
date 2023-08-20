import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from csv import writer
import warnings
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config( page_title='LSM', page_icon=logo)

def get_data():
    signs = pd.read_csv("lsm_senas.csv")
    all_signs = signs['Palabra(s)'].to_list()
    all_temas = signs['Tema'].unique()
    return signs, all_signs, all_temas

st.markdown(f"<h4 style='text-align: center;'>AGREGAR PALABRA</h4>", unsafe_allow_html=True)
signs, all_signs, all_temas = get_data()
all_t = np.append(all_temas, 'Otro')

password = st.text_input('Contraseña:')

if password == 'cultura':  
    with st.form(key='agregar_palabra',clear_on_submit= True):
        st.subheader("Agregar Palabra")
        palabras = st.text_input('Palabra')
        tema_selectbox = st.empty()
        tema_optional_text = st.empty()
        video1 = st.text_input('Video 1')
        video2 = st.text_input('Video 2')
        video3 = st.text_input('Video 3')

        submitted = st.form_submit_button("Submit")

    with tema_selectbox:
        tema = st.selectbox('Selecciona los temas a estudiar', all_t)

    with tema_optional_text:
        if tema == 'Otro':
            tema = st.text_input('Tema')

    new_sign = [palabras, tema, video1, video2, video3]

    if submitted:
        with open('lsm_senas.csv', 'a', newline = '') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new_sign)
            f_object.close()