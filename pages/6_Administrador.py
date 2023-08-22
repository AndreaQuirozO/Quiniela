import streamlit as st
import streamlit_toggle as tog
from PIL import Image
import pandas as pd
import numpy as np
from csv import writer
import warnings
import os
warnings.filterwarnings('ignore')

logo = Image.open('logo.png')
st.set_page_config( page_title='LSM', page_icon=logo)


def get_data():
    participantes = pd.read_csv("participantes.csv")
    return participantes


contrasena = 'k'
st.markdown(f"<h3 style='text-align: center;'>Ajustes</h3>", unsafe_allow_html=True)

password = st.text_input('Contraseña:')

if password == contrasena:
    agregar, resetear, bloquer = st.container(), st.container(), st.container()

    with agregar:
        st.write('#')
        st.markdown(f"<h4 style='text-align: center;'>Agregar Participante</h4>", unsafe_allow_html=True)
        with st.form(key='agregar_palabra',clear_on_submit= True):
            st.subheader("Agregar Participante")
            participante = st.text_input('Nombre')
            contra_p = st.text_input('Contraseña')

            submitted = st.form_submit_button("Submit")

        new_participant = [participante, contra_p, 0]

        if (len(participante) > 0 and len(contra_p)) and submitted:
            with open('participantes.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(new_participant)
                f_object.close()

            fixtures = st.session_state.fixtures

            with open(str(participante) + '_Resultados.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                fixtures.to_csv(f_object, index=False)  # Automatically skips missing keys
                f_object.close()
        else:
            if submitted and not (len(participante) > 0):
                st.markdown(f"<h4 style='text-align: center;'>Nombre requerido</h4>", unsafe_allow_html=True)


    with resetear:
        st.write('#')
        a, b, c = st.columns(3)
        with b:
            if st.button('Resetear Participantes'):
                df = get_data()
                for i in df['Nombre']:
                    os.remove(str(i) + '_Resultados.csv')
                df.drop(df.index, inplace=True)
                df.to_csv('participantes.csv', index=False)
                if len(get_data()) < 1:
                    st.write('Participantes reseteados')

    with resetear:
        st.write('#')
        st.markdown(f"<h4 style='text-align: center;'>Bloquear resultados</h4>", unsafe_allow_html=True)
        a, b, c = st.columns([1, 3.5, 4])
        with b:
            if tog.st_toggle_switch(label=" ",
                                 key="bloquear",
                                 default_value=st.session_state.bloquear_res,
                                 label_after=False,
                                 inactive_color='#D3D3D3',
                                 active_color="#11567f",
                                 track_color="#29B5E8"
                                 ):
                bloquear_resultados = True
                st.session_state.bloquear_res = True
            else:
                bloquear_resultados = False
                st.session_state.bloquear_res = False

        if bloquear_resultados:
            st.markdown(f"<p style='text-align: center;'>Resultados bloqueados</p>", unsafe_allow_html=True)



