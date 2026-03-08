import os
import sys
import time
import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image

import tkventana
import tkinter as tk
from tkinter import filedialog
import requests
import json
import pandas as pd




ruta_csv = os.path.join("Streamlit", "Assets", "dataset_ml.csv")

if os.path.exists(ruta_csv):
    data_grafica = pd.read_csv(ruta_csv)
    st.line_chart(data_grafica.set_index("frame"))
else:
    st.info("Esperando a que el Backend genere el dataset...")

def seleccionar_archivo_local():
    root = tk.Tk()
    root.withdraw()
    # Forzar que la ventana salga al frente
    root.attributes('-topmost', True)
    ruta = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    root.destroy()
    return ruta

# Configuración de Tesseract local (la que hiciste en la carpeta teser)
pytesseract.pytesseract.tesseract_cmd = r'teser\tesseract.exe'


st.set_page_config(layout="wide", page_title="Gamer Diagnostic Tool")
st.title("Gamer Diagnostic Tool 🎮")

# --- SECCIÓN DE ENTRADA ---
with st.expander("📤 Sube tus datos de partida"):
    st.write("Aquí puedes subir los archivos generados por nuestro motor de análisis.")
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        yt_link = st.text_input("Link de YouTube de tu Gameplay", "https://youtu.be/9qUf8iQfjvQ")
    
    with col_input2:
        uploaded_file = st.file_uploader("Sube tu archivo .CSV o .JSON extraído", type=['csv', 'json'])

    # 1. Widget de carga restringido a MP4
    with st.expander("📂 Selección de Gameplay Local"):
        st.write("Selecciona tu archivo y define los 7 momentos.")
        
        # Botón para abrir el explorador de Windows
        if st.button("📁 Abrir Explorador de Archivos"):
            ruta = seleccionar_archivo_local()
            if ruta:
                st.session_state.ruta_seleccionada = ruta
        
        # Mostrar la ruta seleccionada (solo lectura para que no la editen mal)
        ruta_final = st.session_state.get('ruta_seleccionada', "")
        st.text_input("Ruta cargada:", value=ruta_final, disabled=True)

        # Slots de tiempo (tus 7 momentos)
        rangos_seleccionados = []
        for i in range(1, 8):
            col_ini, col_fin = st.columns(2)
            with col_ini:
                ini = st.number_input(f"M{i} Inicio", min_value=0, key=f"ini_{i}")
            with col_fin:
                fin = st.number_input(f"M{i} Fin", min_value=0, key=f"fin_{i}")
            if fin > ini:
                rangos_seleccionados.append(f"{ini}-{fin}")

        # Botón para disparar al Backend
        if st.button("🚀 Iniciar Procesamiento Maestro"):
            if ruta_final and rangos_seleccionados:
                tiempos_string = ",".join(rangos_seleccionados)
                
                # Enviamos solo la ruta y los tiempos al backend
                params = {"ruta": ruta_final, "tiempos": tiempos_string}
                response = requests.post("http://localhost:8000/procesar-todo/", params=params)
                
                if response.status_code == 200:
                    st.success("✅ Backend trabajando. YOLO está analizando los frames.")
                else:
                    st.error("❌ Error al contactar el backend. Asegúrate de que esté corriendo.")
            

st.divider()
# --- DISEÑO DE PANTALLA ---
col_video, col_stats = st.columns([0.7, 0.3])

with col_video:
    st.subheader("📺 Visualización de tu gameplay")
    # Restauramos el link de YouTube para no consumir RAM local
    # yt_link viene del st.text_input de la sección de entrada
    st.video(yt_link) 
    
    st.divider()

   
    
with col_stats:
    st.subheader("🕵️ Diagnóstico Forense YSM")

    # Definimos la ruta exacta a la gráfica
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_grafica = os.path.join( "Assets", "grafica_ml.png")

    col1, col2 = st.columns(2)

    with col1:
        # --- BLOQUE DE SEGURIDAD PARA LA GRÁFICA ---
       if st.button("Ver Resultados del ML"):
            if os.path.exists(ruta_grafica):
                try:
                    # Abrimos el archivo en modo lectura de bytes ('rb')
                    with open(ruta_grafica, "rb") as file:
                        contenido_imagen = file.read()
                    
                    # Pasamos los bytes directamente a Streamlit
                    st.image(contenido_imagen, caption="Análisis generado por el ML")
                    st.success("¡Data visualizada correctamente!")
                    
                except Exception as e:
                    st.error(f"Error de acceso: {e}")
                    st.info("Intenta darle clic de nuevo en 1 segundo, el sistema está liberando el archivo.")
            else:
                st.error("La gráfica aún no ha sido generada por el Backend.")

   