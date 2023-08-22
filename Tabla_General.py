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

url2 = 'https://forzafootball.com/tournament/womens-wc-566'
url1 = 'https://forzafootball.com/tournament/national-womens-soccer-league-1221'
url = 'https://forzafootball.com/tournament/women%E2%80%99s-super-league-1549'


@st.cache_data
def get_data(url):
    cookies = dict(language='en')
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    tournament = soup.find(class_='EntityHeader_EntityHeader-title__qZ_X8 EntityHeader-title-global-js').get_text()
    tournament_image = soup.find(class_='EntityHeader_EntityHeader-image__elwjc').find('img')['src']

    return tournament, tournament_image

@st.cache_data
def get_data_fixtures(url):
    cookies = dict(language='en')
    url = url + '/fixtures'
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    scr = soup.find('script', id="__NEXT_DATA__")
    json_object = json.loads(scr.contents[0])
    dates = []
    for i in json_object['props']['pageProps']['fixtures']:
        for j in range(len(json_object['props']['pageProps']['fixtures'][i])):
            dates.append(json_object['props']['pageProps']['fixtures'][i][j]['kickoff_at'])

    for i in range(len(dates)):
        dates[i] = datetime.fromisoformat(dates[i][:-1]).astimezone(pytz.timezone('Etc/GMT+12'))
        # d.strftime('%Y-%m-%d %H:%M:%S')
        # d.strftime('%A')

    s = soup.find_all('div', class_='section')
    matches = []
    m = 0
    for st in s:
        stage = st.find(class_='MatchlistHeader_MatchlistHeader-meta__p_OwG').text
        for match in st.find_all(class_='MatchlistItem_MatchlistItem-details__BSPgK'):
            status = match.find('div', 'MatchlistItem_MatchlistItem-status__IqQLN').text
            t1, t2 = match.find_all(class_='MatchlistItem_MatchlistItem-teams-name__ZAe9M')
            team1 = t1.get_text()
            team2 = t2.get_text()
            s1, s2 = match.find('div', class_='MatchlistItem_MatchlistItem-score__p6yHr').find_all("span")
            score1 = s1.get_text()
            score2 = s2.get_text()
            img1, img2 = match.find_all('div', 'MatchlistItem_MatchlistItem-logo__7mEHa')
            image1 = img1.find('img')['src']
            image2 = img2.find('img')['src']
            date = dates[m]
            matches.append([stage, status, date, team1, image1, team2, image2, score1, score2])
            m += 1

    fix = pd.DataFrame(matches, columns=['Stage', 'Status', 'Date',
                                         'Team1', 'Image1', 'Team2', 'Image2', 'Score1', 'Score2'])

    return fix

@st.cache_data
def get_data_results(url):
    url = url + '/results'
    cookies = dict(language='en')
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    scr = soup.find('script', id="__NEXT_DATA__")
    json_object = json.loads(scr.contents[0])
    dates = []
    for i in json_object['props']['pageProps']['results']:
        for j in range(len(json_object['props']['pageProps']['results'][i])):
            dates.append(json_object['props']['pageProps']['results'][i][j]['kickoff_at'])

    for i in range(len(dates)):
        dates[i] = datetime.fromisoformat(dates[i][:-1]).astimezone(pytz.timezone('Etc/GMT+12'))
        # d.strftime('%Y-%m-%d %H:%M:%S')
        # d.strftime('%A')

    s = soup.find_all('div', class_='section')
    matches = []
    m = 0
    for st in s:
        stage = st.find(class_='MatchlistHeader_MatchlistHeader-meta__p_OwG').text
        for match in st.find_all(class_='MatchlistItem_MatchlistItem-details__BSPgK'):
            status = match.find('div', 'MatchlistItem_MatchlistItem-status__IqQLN').text
            t1, t2 = match.find_all(class_='MatchlistItem_MatchlistItem-teams-name__ZAe9M')
            team1 = t1.get_text()
            team2 = t2.get_text()
            s1, s2 = match.find('div', class_='MatchlistItem_MatchlistItem-score__p6yHr').find_all("span")
            score1 = s1.get_text()
            score2 = s2.get_text()
            img1, img2 = match.find_all('div', 'MatchlistItem_MatchlistItem-logo__7mEHa')
            image1 = img1.find('img')['src']
            image2 = img2.find('img')['src']
            date = dates[m]
            matches.append([stage, status, date, team1, image1, team2, image2, score1, score2])
            m += 1

    res = pd.DataFrame(matches, columns=['Stage', 'Status', 'Date',
                                         'Team1', 'Image1', 'Team2', 'Image2', 'Score1', 'Score2'])

    return res

def get_tabla_general():
    tg = pd.read_csv('participantes.csv')
    tg.index += 1
    tg.drop('Contraseña', axis=1, inplace=True)
    tg = tg.sort_values(by=['Puntos'], ascending=False)
    return tg


with header:
    tournament, tournament_image = get_data(url)
    fixtures = get_data_fixtures(url)
    results = get_data_results(url)
    st.session_state.tournament = tournament
    st.session_state.fixtures = fixtures
    st.session_state.results = results
    a, b, c = st.columns(3)
    with st.columns(5)[2]:
        st.image(tournament_image, use_column_width=True)
    st.markdown(f"<h1 style='text-align: center;'>{tournament}</h1>", unsafe_allow_html=True)

# tabla_general, fixtures = st.columns(2)

with tabla_general:
    tab_grl = get_tabla_general()
    st.markdown(f"<h4 style='text-align: center;'>Tabla General</h4>", unsafe_allow_html=True)
    st.table(tab_grl)
