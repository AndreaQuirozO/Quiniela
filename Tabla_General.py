import streamlit as st
from PIL import Image
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pytz
import warnings
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config(page_title='Quiniela ', page_icon=logo)

header = st.container()
tabla_general = st.container()

hide_menu = """
<style>
    #MainMenu {
        visibility:hidden;}
    footer {
        visibility: hidden;}
</style>
"""

def get_data():
    cookies = dict(language='en')
    url = 'https://forzafootball.com/tournament/womens-wc-566/fixtures'
    url = 'https://forzafootball.com/tournament/national-womens-soccer-league-1221/fixtures'
    url1 = 'https://forzafootball.com/tournament/women%E2%80%99s-super-league-1549/fixtures'
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    tournament = soup.find(class_='EntityHeader_EntityHeader-title__qZ_X8 EntityHeader-title-global-js').get_text()
    tournament_image = soup.find(class_='EntityHeader_EntityHeader-image__elwjc').find('img')['src']


    return tournament, tournament_image


with header:
    tournament, tournament_image = get_data()
    with st.columns(3)[1]:
        st.image(tournament_image, width=200)
    st.markdown(f"<h1 style='text-align: center;'>Quiniela</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{tournament}</h1>", unsafe_allow_html=True)


#tabla_general, fixtures = st.columns(2)

with tabla_general:
    st.markdown(f"<h1 style='text-align: center;'>Tabla General</h1>", unsafe_allow_html=True)
    tab_grl = pd.DataFrame(columns=['Nombre', 'Puntos'], index=range(1, 13))
    st.table(tab_grl)






