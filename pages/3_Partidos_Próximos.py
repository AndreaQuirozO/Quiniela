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

fixtures = st.session_state.fixtures

upcoming = st.container()

with upcoming:
    st.markdown(f"<h2 style='text-align: center;'>Partidos próximos</h2>", unsafe_allow_html=True)
    st.write('###')
    global_stage = ''

    if fixtures.empty:
        st.write('###')
        st.markdown(f"<h3 style='text-align: center;'>No hay partidos próximos</h3>", unsafe_allow_html=True)
    else:

        for index, row in fixtures.iterrows():
            stage = row['Stage']
            status = row['Status']
            date = row['Date']
            team1 = row['Team1']
            team2 = row['Team2']
            score1 = row['Score1']
            score2 = row['Score2']
            image1 = row['Image1']
            image2 = row['Image2']

            if stage != global_stage:
                global_stage = stage
                st.markdown(f"<h3 style='text-align: center;'>{stage}</h3>", unsafe_allow_html=True)
                st.write("###")

            stat, ts = st.columns([2,6])

            with stat:
                if status == '':
                    date_day = date.strftime('%d %b')
                    date_hour = date.strftime("%I:%M %p")
                    d, h = st.container(), st.container()
                    with d:
                        st.write(date_day)
                    with h:
                        st.write(date_hour)
                else:
                    st_m, sc = st.columns([2, 2])

                    with st_m:
                        a, b, c = st.container(), st.container(), st.container()
                        with a:
                            st.write('')
                        with b:
                            st.write(status)
                        with c:
                            st.write('')

                    with sc:
                        s1, s2 = st.container(), st.container()
                        with s1:
                            st.write(score1)
                        with s2:
                            st.write(score2)

            with ts:
                img, t = st.columns([2, 5])
                with img:
                    img1, img2 = st.container(), st.container()
                    with img1:
                        st.image(image1, width=25)
                    with img2:
                        st.image(image2, width=25)
                with t:
                    t1, t2 = st.container(), st.container()
                    with t1:
                        st.write(team1)
                    with t2:
                        st.write(team2)

            st.divider()