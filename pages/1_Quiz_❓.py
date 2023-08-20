import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import random
from csv import writer
import warnings
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config( page_title='LSM', page_icon=logo)

@st.cache_data
def get_data():
    s = pd.read_csv("lsm_senas.csv")
    all_signs = s['Palabra(s)'].to_list()
    all_temas = s['Tema'].unique()
    signs = s.sample(frac = 1)
    return signs, all_signs, all_temas

def next(): st.session_state.counter += 1
def prev(): st.session_state.counter -= 1
def reset(): st.session_state.counter = 0

st.markdown(f"<h1 style='text-align: center;'>QUIZ</h1>", unsafe_allow_html=True)
st.write('')
signs, all_signs, all_temas = get_data()

temas = st.multiselect('Selecciona los temas a estudiar', all_temas)
quiz_df = pd.DataFrame(columns = signs.columns.to_list())
for i in temas:
    quiz_df = pd.concat([quiz_df, signs[signs['Tema'] == i]], axis=0, ignore_index=True)
preguntas = quiz_df['Palabra(s)'].to_list()
n_preg = len(preguntas)
video_si_no = st.radio(
    "Mostrar videos para la respuesta",
    ('Sí', 'No'))


container = st.empty()
cols = st.columns(2)
with cols[1]: st.button("→", on_click=next, use_container_width=True)
with cols[0]: st.button("←", on_click=prev, use_container_width=True)
st.write('')
st.write('')
st.write('')

with container.container():
    try:
        preg = preguntas[st.session_state.counter%n_preg]
        info = signs[signs['Palabra(s)'] == preg]
        vid1 = info.iloc[0][2]
        vid2 = info.iloc[0][3]
        vid3 = info.iloc[0][4]
        st.write('')
        st.write('')
        st.write('')
        if video_si_no == 'Sí':
            cols = st.columns(2)
            with cols[0]: 
                st.markdown(f"<h3 style='text-align: center;'>{preg}</h3>", unsafe_allow_html=True)
            with cols[1]:
                st.video(vid1)
                if not pd.isnull(vid2):
                    if st.button('Ver opción 2'):
                        st.video(vid2)
                if not pd.isnull(vid3):
                    if st.button('Ver opción 3'):
                        st.video(vid3)
        if video_si_no == 'No':
            st.markdown(f"<h3 style='text-align: center;'>{preg}</h3>", unsafe_allow_html=True)
    except:
        st.write('')
        st.write('')
        st.write('')
        st.markdown(f"<h3 style='text-align: center;'>Selecciona un tema</h3>", unsafe_allow_html=True)
        reset()

c1, c2, c3 = st.columns(3)
with c2:
    if st.button("Volver a revolver palabras", use_container_width=True):
        st.cache_data.clear()


