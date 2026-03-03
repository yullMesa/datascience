import joblib
import streamlit as st
import pandas as pd
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'teser\tesseract.exe'
# 1. Configuración de pantalla ancha (Platzi Style)
st.set_page_config(layout="wide", page_title="LoL Analytics Academy")

# 2. Título del Proyecto
st.title("Gamer Diagnostic Tool 🎮")

uploaded_file = st.file_uploader("Sube tus estadísticas (CSV o JSON)")

mi_modelo = joblib.load('tu_modelo_entrenado.pkl')
if uploaded_file:
    user_data = pd.read_csv(uploaded_file)
    # Aquí corres tu modelo de ML que ya tienes entrenado con la data "Maestra"
    resultado = mi_modelo.predict(user_data)
    st.write(f"Tu nivel de desempeño es: {resultado}")

# 3. Definimos las columnas (70% para el video, 30% para las estadísticas)
col_video, col_stats = st.columns([0.7, 0.3])

with col_video:
    # Al no haber errores, el video se verá grande de nuevo
    st.video("https://youtu.be/pyuiUd2L9CA") 
    st.write("### Coach Insights")
    st.info("Diamond players focus on Gold Diff in the first 10 minutes.")

with col_stats:
    st.header("Live Metrics")
    try:
        # IMPORTANTE: Nota la 'A' mayúscula en 'Archive' como en tu carpeta
        df = pd.read_csv('../Archive/high_diamond_ranked_10min.csv')
        
        # Calculamos una métrica real del dataset
        avg_gold = df['blueGoldDiff'].mean()
        st.metric(label="Avg Gold Diff (Blue Team)", value=f"{avg_gold:.2f}")
        
        # Gráfica de barras con las primeras muertes del dataset
        st.bar_chart(df[['blueKills', 'redKills']].head(15))
        
        st.success("✅ Data Loaded Successfully!")
    except FileNotFoundError:
        st.error("⚠️ No se encontró el archivo. Revisa si la carpeta es 'Archive' o 'archive'.")