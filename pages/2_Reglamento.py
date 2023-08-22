import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import random
from csv import writer
import warnings
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config(page_title='Quiniela ', page_icon=logo)


st.markdown(f"<h2 style='text-align: center;'>Reglamento</h2>", unsafe_allow_html=True)

st.write('#')
st.write('#### Puntos:')
st.write('- Final: 5 puntos por acertar el ganador, +5 puntos por acertar el marcador')
st.write('- Semifinal: 5 puntos por acertar el ganador, +3 puntos por acertar el marcador')
st.write('- Cuartos de final: 5 puntos por acertar el ganador, +2 puntos por acertar el marcador')
st.write('- Octavos de final: 3 puntos por acertar el ganador, +1 puntos por acertar el marcador')
st.write('- Fase de grupos: 1 punto por acertar el ganador, +1 puntos por acertar el marcador')

