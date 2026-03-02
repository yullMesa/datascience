import streamlit as st
import pandas as pd

# Configuración de la página para que ocupe todo el ancho (Modo Cine)
st.set_page_config(layout="wide", page_title="TFT Data Analytics - Platzi Style")

# Estilo CSS para que se parezca a Platzi (Fondo oscuro y bordes redondeados)
st.markdown("""
    <style>
    .main {
        background-color: #121f3d;
        color: white;
    }
    stVideo {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título del Proyecto (Usa Inglés para practicar tu Elementary 3)
st.title("🎮 TFT Match Analyzer: Pro vs Your Stats")

# Creamos las dos columnas: una grande para el video y una lateral para la data
col_video, col_data = st.columns([0.7, 0.3])

with col_video:
    st.subheader("Match Replay")
    # Aquí pegas el link de tu video de YouTube
    url_youtube = "https://www.youtube.com/watch?v=tu_link_aqui" 
    st.video(url_youtube)
    
    st.info("💡 Insight: In this round, your gold management was 15% below Challenger level.")

with col_data:
    st.subheader("Live Analytics")
    # Simulamos una métrica de comparación con el dataset de Challengers
    st.metric(label="Win Probability", value="65%", delta="+5% vs Last Round")
    
    # Un gráfico de barras de prueba (luego lo conectamos al CSV)
    chart_data = pd.DataFrame({
        'Stat': ['Gold', 'Health', 'Level'],
        'You': [40, 85, 6],
        'Challenger': [50, 90, 7]
    }).set_index('Stat')
    
    st.bar_chart(chart_data)
    
    st.write("### Current Synergy")
    st.success("✨ KDA - Active")