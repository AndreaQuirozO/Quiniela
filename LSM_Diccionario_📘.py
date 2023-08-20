import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from csv import writer
import warnings
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config( page_title='LSM', page_icon=logo)

header = st.container()
dic = st.container()

hide_menu = """
<style>
    #MainMenu {
        visibility:hidden;}
    footer {
        visibility: hidden;}
</style>
"""
def get_data():
    signs = pd.read_csv("lsm_senas.csv")
    all_signs = signs['Palabra(s)'].to_list()
    all_temas = signs['Tema'].unique()
    return signs, all_signs, all_temas

with header:
    with st.columns(3)[1]:
        st.image("logo.png", width=200)
    st.markdown(f"<h1 style='text-align: center;'>LENGUA DE SEÑAS MEXICANA</h1>", unsafe_allow_html=True)
    signs, all_signs, all_temas = get_data()


with dic:
    st.write('')
    palabra = dic.selectbox('Palabra:', options=all_signs, index=28)
    info = signs[signs['Palabra(s)'] == palabra]
    word = info.iloc[0][0]
    tema = info.iloc[0][1]
    vid1 = info.iloc[0][2]
    vid2 = info.iloc[0][3]
    vid3 = info.iloc[0][4]
    st.write('')
    st.markdown(f"<h2 style='text-align: center;'>{word}</h2>", unsafe_allow_html=True)
    st.video(vid1)
    if not pd.isnull(vid2):
        st.video(vid2)
    if not pd.isnull(vid3):
        st.video(vid3)




