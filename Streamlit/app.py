import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image

# Configuración de Tesseract local (la que hiciste en la carpeta teser)
pytesseract.pytesseract.tesseract_cmd = r'teser\tesseract.exe'

st.set_page_config(layout="wide", page_title="Gamer Diagnostic Tool")
st.title("Gamer Diagnostic Tool 🎮")

# --- SECCIÓN DE ENTRADA ---
with st.expander("📤 Sube tus datos de partida"):
    st.write("Aquí puedes subir los archivos generados por nuestro motor de análisis.")
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        yt_link = st.text_input("Link de YouTube de tu Gameplay", "https://youtu.be/pyuiUd2L9CA")
    
    with col_input2:
        uploaded_file = st.file_uploader("Sube tu archivo .CSV o .JSON extraído", type=['csv', 'json'])

st.divider()

# --- DISEÑO DE PANTALLA ---
col_video, col_stats = st.columns([0.7, 0.3])

with col_video:
    st.subheader("Análisis de Video")
    # El video cambia según el link que ponga el usuario arriba
    st.video(yt_link)

with col_stats:
    st.subheader("Live Metrics")
    st.info("💡 **Instrucciones:** Una vez subas tu archivo CSV, aquí compararemos tus métricas con el modelo maestro.")
    
    # Botón que mencionaste para la explicación
    if st.button("¿Cómo obtener mis datos?"):
        st.write("1. Procesa tu video con nuestro script de Tesseract.")
        st.write("2. Exporta el archivo CSV resultante.")
        st.write("3. Súbelo en la sección de arriba para recibir el diagnóstico de la IA.")