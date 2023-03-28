import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import csv

# Leer el archivo CSV y crear una lista de juegos y un dataframe de consolas
df = pd.read_csv("Juegos.csv")
nombres_compradores = df['Juego'].unique().tolist()
consolas_df = df[['Juego', 'Consola']].drop_duplicates()

# Definir las variables de sesión para la consola seleccionada, la fecha de inicio y la duración
if 'consola_seleccionada' not in st.session_state:
    st.session_state.consola_seleccionada = ''
if 'tiempo_inicio' not in st.session_state:
    st.session_state.tiempo_inicio = None
if 'duracion' not in st.session_state:
    st.session_state.duracion = timedelta(minutes=30)

# Mostrar el formulario para agregar renta
st.write('Agregar renta')
nombre_comprador = st.selectbox("Nombre del juego", nombres_compradores)

# Obtener las consolas disponibles para el juego seleccionado
consolas_juego = consolas_df[consolas_df['Juego'] == nombre_comprador]['Consola'].unique().tolist()

# Mostrar el selectbox de consolas y recuperar la consola seleccionada (si existe)
consola_seleccionada = st.selectbox("Seleccione la consola", consolas_juego, index=consolas_juego.index(st.session_state.consola_seleccionada) if st.session_state.consola_seleccionada in consolas_juego else 0)

# Guardar la consola seleccionada en session_state
st.session_state.consola_seleccionada = consola_seleccionada

# Si la fecha de inicio no ha sido seleccionada, obtener la fecha y hora actual y guardarla en session_state
if st.session_state.tiempo_inicio is None:
    st.session_state.tiempo_inicio = datetime.now()

# Mostrar botones para agregar o quitar 30 minutos a la duración
if st.button('+30 min'):
    st.session_state.duracion += timedelta(minutes=30)
if st.button('-30 min'):
    st.session_state.duracion -= timedelta(minutes=30)

# Mostrar un widget para seleccionar la fecha final
fecha_fin = datetime.today()
hora_fin = st.time_input("Ingrese la hora final", value=(st.session_state.tiempo_inicio + st.session_state.duracion).time())
fecha_fin = fecha_fin.replace(hour=hora_fin.hour, minute=hora_fin.minute, second=hora_fin.second)

# Mostrar el botón de submit
submit_button = st.button('Agregar renta')

# Si el botón de submit fue presionado, mostrar la información que se va a agregar al archivo CSV
if submit_button:
    consola_seleccionada = pd.Series(consola_seleccionada)
    rentas_df = pd.read_csv('rentasactuales.csv')
    consola_rentada = consola_seleccionada.isin(rentas_df['Consola']).any()
    if consola_rentada:
        st.write("Consola en uso")
    else:
        st.write("Confirmación de renta:")
        st.write(f"Juego: {nombre_comprador}")
        st.write(f"Consola: {consola_seleccionada}")
        st.write(f"Fecha de inicio: {st.session_state.tiempo_inicio}")
        st.write(f"Fecha de fin: {fecha_fin}")

        # Agregar la información en el archivo "rentasactuales.csv"
        with open("rentasactuales.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([consola_seleccionada, nombre_comprador, st.session_state.tiempo_inicio, fecha_fin])
