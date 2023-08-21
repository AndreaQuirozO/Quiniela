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

upcoming = st.container()

def get_data():
    cookies = dict(language='en')
    url = 'https://forzafootball.com/tournament/womens-wc-566/fixtures'
    url = 'https://forzafootball.com/tournament/national-womens-soccer-league-1221/fixtures'
    url1 = 'https://forzafootball.com/tournament/women%E2%80%99s-super-league-1549/fixtures'
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    tournament = soup.find(class_='EntityHeader_EntityHeader-title__qZ_X8 EntityHeader-title-global-js').get_text()
    tournament_image = soup.find(class_='EntityHeader_EntityHeader-image__elwjc').find('img')['src']

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

    return tournament, tournament_image, fix

tournament, tournament_image, fix = get_data()


with upcoming:
    st.markdown(f"<h1 style='text-align: center;'>Partidos próximos</h1>", unsafe_allow_html=True)
    st.write('###')
    global_stage = ''

    if fix.empty:
        st.write('###')
        st.markdown(f"<h3 style='text-align: center;'>No hay partidos próximos</h3>", unsafe_allow_html=True)
    else:

        for index, row in fix.iterrows():
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