import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
from vision import analizar_frames_ysm
import tkventana
import tkinter as tk
from tkinter import filedialog
import requests


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
        if st.button("🚀 Procesar Momentos"):
            if ruta_final and rangos_seleccionados:
                tiempos_string = ",".join(rangos_seleccionados)
                params = {"ruta": ruta_final, "tiempos": tiempos_string}
                
                try:
                    # El backend recibe solo el texto de la ruta
                    response = requests.post("http://localhost:8000/procesar-local/", params=params)
                    if response.status_code == 200:
                        st.success("✅ ¡Vinculado! El backend está trabajando en el archivo original.")
                except Exception as e:
                    st.error(f"Error: {e}")

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
    # Mensaje de estado que pusimos antes
    st.warning("⚠️ **Estado:** Análisis asíncrono activado (Intervalo: 7s).")
    
    if st.button("🚀 Iniciar Escaneo Forense"):
        with st.spinner("Tesseract analizando momentos clave..."):
            # Llamamos a la función optimizada
            logs = analizar_frames_ysm("Streamlit/Assets/frames_extraidos")
            
            if logs:
                for l in logs:
                    # Mostramos el resultado con estilo hacker
                    st.code(f"🔍 [{l['frame']}] Detectado: {l['dato']}")
            else:
                st.error("No se detectó texto legible en los rangos seleccionados.")





