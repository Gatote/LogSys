import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import os.path

def main():
    # Definir el encabezado y subtítulo de la página
    st.title("Aplicación de Recordatorios")
    
    # Si no existe un archivo CSV, no permitir la creación de nuevos recordatorios
    if not os.path.isfile("recordatorios.csv"):
        st.write("No hay recordatorios guardados. Crea uno nuevo para empezar.")
        return

    st.write("Recordatorios guardados:")
    df = pd.read_csv("recordatorios.csv")
    st.dataframe(df)

    # Definir el formulario para ingresar un nuevo recordatorio
    header = st.text_input("Encabezado del recordatorio:")
    description = st.text_area("Descripción del recordatorio:")
    date = st.date_input("Fecha del recordatorio:", datetime.now().date())

    # Definir el estado por defecto
    status = "Pendiente"

    # Si se ha ingresado un encabezado, descripción y fecha, guardar el recordatorio en un archivo CSV
    if st.button("Guardar recordatorio", key=uuid.uuid1()):
        data = {"Encabezado": [header], "Descripción": [description], "Fecha": [date], "Estado": [status]}
        df = pd.DataFrame(data)
        df.to_csv("recordatorios.csv", mode="a", index=False, header=not st.session_state.get('csv_written', False))
        st.success("¡El recordatorio ha sido guardado con éxito!")
        st.session_state.csv_written = True
