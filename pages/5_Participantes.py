import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from csv import writer
import warnings
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config(page_title='Quiniela ', page_icon=logo)



def get_data():
    participantes = pd.read_csv("participantes.csv")
    nombres = participantes['Nombre'].to_list()
    return participantes, nombres

def get_participants_results(Nombre):
    results = pd.read_csv(Nombre + '_Resultados.csv')
    return results



if not st.session_state.bloquear_res:
    header, sign_in = st.container(), st.container()

    with header:
        participantes, nombres = get_data()
        st.markdown(f"<h2 style='text-align: center;'>Agregar Resultados</h2>", unsafe_allow_html=True)

    with sign_in:
        if len(nombres) > 0:
            nombre = st.selectbox('Nombre', nombres)
            password = st.text_input('Contraseña:')
            if len(password) > 0:
                if password == participantes[participantes['Nombre'] == nombre]['Contraseña'].iloc[0]:
                    st.markdown(f"<h4 style='text-align: center;'>Hola {nombre}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'>Ingresa tus resutados en las columnas <i>Goles 1</i> y <i>Goles 2</i></p>", unsafe_allow_html=True)
                    participants_results = get_participants_results(nombre)
                    participants_results['Date'] = pd.to_datetime(participants_results['Date'])
                    participants_results['Date'] = participants_results['Date'].dt.strftime("%d %b %I:%M %p")
                    participants_results.drop(columns=['Status', 'Image1', 'Image2'], inplace=True)
                    participants_results.rename(columns={'Stage': 'Etapa', 'Date': 'Fecha',
                                                         'Team1': 'Equipo 1', 'Team2': 'Equipo 2',
                                                         'Score1': 'Goles 1', 'Score2': 'Goles 2'}, inplace=True)
                    participants_results['Goles 1'] = ''
                    participants_results['Goles 2'] = ''
                    edited_pr = st.data_editor(participants_results,
                                                            use_container_width=False, num_rows="fixed",
                                                            disabled=['Etapa','Fecha','Equipo 1','Equipo 2'])

                else:
                    st.markdown(f"<h4 style='text-align: center;'>Contraseña incorrecta</h4>", unsafe_allow_html=True)

        else:
            st.write('#')
            st.write('#')
            st.markdown(f"<p style='text-align: center;'>No hay participantes</p>", unsafe_allow_html=True)

else:
    st.markdown(f"<h2 style='text-align: center;'>Agregar Resultados Bloqueado</h2>", unsafe_allow_html=True)