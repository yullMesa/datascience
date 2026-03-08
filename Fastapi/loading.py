import os
import sys
import pandas as pd
from fastapi import FastAPI, BackgroundTasks
import cv2
import json
from ultralytics import YOLO
import pytesseract
import torch
import shutil

app = FastAPI()

# --- CONFIGURACIÓN DINÁMICA DE RUTAS ---

# 1. Detectamos dónde está 'loading.py' (dentro de la carpeta FastAPI)
DIRECTORIO_BACKEND = os.path.dirname(os.path.abspath(__file__))

# 2. Subimos un nivel a la RAÍZ del proyecto
RAIZ_PROYECTO = os.path.dirname(DIRECTORIO_BACKEND)

# 3. Construimos la ruta hacia la carpeta de Assets en Streamlit
# Unimos: RAIZ -> Streamlit -> Assets -> frames_extraidos
OUTPUT_DIR = os.path.join(RAIZ_PROYECTO, "Streamlit", "Assets", "frames_extraidos")

ruta_tesseract_exe = os.path.join(RAIZ_PROYECTO, "teser", "tesseract.exe")

# 3. LE ASIGNAMOS LA RUTA A LA LIBRERÍA (Esto quita el error de pytesseract.py)
pytesseract.pytesseract.tesseract_cmd = ruta_tesseract_exe

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"✅ Tesseract vinculado en: {ruta_tesseract_exe}")

# 4. Verificación de seguridad
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✅ Carpeta vinculada con éxito en: {OUTPUT_DIR}")
else:
    print(f"🔗 Conexión establecida con la carpeta de Assets: {OUTPUT_DIR}")

# --- CARGA DE MODELOS ---
model = YOLO('yolov8n.pt')

ruta_actual = os.path.dirname(os.path.abspath(__file__)) # Esto es 'Fastapi'
ruta_raiz = os.path.dirname(ruta_actual) # Esto sube un nivel a 'datascience'

# 2. Agregamos la raíz al sistema para que vea la carpeta 'ML'
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

# 3. Importamos usando el nombre exacto de tu carpeta (asegúrate que sea ML en mayúsculas)
try:
    from Ml.Transformar import analizar_y_graficar
    print("✅ Módulo ML cargado con éxito")
except Exception as e:
    print(f"❌ Error al cargar ML: {e}")

def proceso_maestro_ysm(video_path, rangos):
    # --- ETAPA 1: EXTRACCIÓN ---
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Primero guardamos TODAS las imágenes
    for r in rangos:
        inicio, fin = map(int, r.split('-'))
        frame_actual = int(inicio * fps)
        frame_limite = int(fin * fps)
        salto = int(fps * 7)
        
        while frame_actual <= frame_limite:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_actual)
            ret, frame = cap.read()
            if not ret: break
            nombre = f"moment_{frame_actual}.jpg"
            cv2.imwrite(os.path.join(OUTPUT_DIR, nombre), frame)
            frame_actual += salto

    cap.release()

    print("✅ Etapa 1 completa: Frames guardados.")

    print(f"🔍 Estoy buscando archivos en: {os.path.abspath(OUTPUT_DIR)}")

    import time
    time.sleep(2)
    # Ahora sí leemos la carpeta porque ya tiene archivos
    lista_fotos = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".jpg")]

    if not lista_fotos:
        print("⚠️ Error: No se encontraron fotos para analizar.")
        return
    
    # --- ETAPA 2: YOLO Y TESSERACT (Turno de la GPU y luego CPU) ---
    datos_partida = []

    # Revisa que tu bucle se vea así:
    # --- ETAPA 2: VERIFICACIÓN ---
    lista_fotos = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".jpg")]
    print(f"🔍 Buscando fotos en: {OUTPUT_DIR}")
    print(f"📸 Fotos encontradas: {len(lista_fotos)}")

    if not lista_fotos:
        print("❌ Error: No hay fotos para procesar. El JSON quedará vacío.")
        return {"status": "error", "message": "No hay frames"}

    # --- ETAPA 3: YOLO (1660 SUPER) ---
    for foto in lista_fotos:
        img_path = os.path.join(OUTPUT_DIR, foto)
        img = cv2.imread(img_path)
        
        results = model.predict(img, conf=0.4, device=0)
        detecciones_frame = []
        
        for r in results:
            for box in r.boxes:
                obj_nombre = model.names[int(box.cls[0])]
                detecciones_frame.append({
                    "objeto": obj_nombre,
                    "valor": "Lectura OCR" # Aquí va tu lógica de Tesseract
                })
        
        # Guardamos el resultado del frame en la lista principal
        datos_partida.append({"frame": foto, "analisis": detecciones_frame})


    # --- ETAPA 4: GENERAR JSON ---
    
    # Verificamos que realmente hayamos capturado algo
    if not datos_partida:
        print("⚠️ Advertencia: No hay datos para guardar en el JSON.")
        return

    try:
        # Usamos una ruta absoluta para no perdernos en Windows
        ruta_final_json = os.path.join(OUTPUT_DIR, "data_final.json")
        
        with open(ruta_final_json, "w", encoding='utf-8') as f:
            json.dump(datos_partida, f, indent=4, ensure_ascii=False)
            
        print(f"✅ ¡ÉXITO! JSON guardado con {len(datos_partida)} frames en: {ruta_final_json}")
    except Exception as e:
        print(f"❌ Error fatal al escribir el JSON: {e}")
    # ... después de que ya tienes tu lista 'datos_partida' llena ...

    # 1. Llamamos al ML
    # --- loading.py ---
# ... (Después de que termina el bucle de YOLO, donde ya tienes datos_partida llena) ...

# 1. PASO CRÍTICO: El ML genera la gráfica *antes* de borrar los .jpg
# ... (Después de que termina el bucle de YOLO, donde ya tienes datos_partida llena) ...

# === NUEVA LÓGICA DE SEGURIDAD PARA EL ML Y LIMPIEZA ===

    print("🧠 Iniciando Fase de Análisis de Machine Learning...")


    # 1. Inicializamos variables de estado
    veredicto = "Error en Análisis"
    se_genero_grafica = False  # <- ESTA ES LA LLAVE DE SEGURIDAD
    ruta_grafica_final = ""

    try:
        from Ml.Transformar import analizar_y_graficar
        # 2. Intentamos generar la gráfica (enviando solo los datos necesarios)
        print("📊 Generando gráfica de ML con los frames JPG...")
        veredicto, ruta_grafica_final = analizar_y_graficar(datos_partida)
        
        # 3. Verificamos si la imagen realmente se creó en el disco
        if os.path.exists(ruta_grafica_final):
            print(f"✅ Gráfica creada y verificada en: {ruta_grafica_final}")
            se_genero_grafica = True  # ¡Damos permiso para limpiar!
        else:
            print(f"❌ Error: Matplotlib dijo que guardó, pero el archivo no aparece en {ruta_grafica_final}")

    except Exception as e:
        print(f"❌ Error crítico al ejecutar el módulo de ML: {e}")
        veredicto = f"Fallo técnico: {str(e)}"


    # --- ETAPA DE LIMPIEZA CONDICIONAL ---

    # 4. SOLO BORRAMOS SI LA GRÁFICA SE GENERÓ CORRECTAMENTE
    if se_genero_grafica:
        print("🧹 Gráfica verificada. Iniciando limpieza de frames JPG temporales...")
        cantidad_borrada = 0
        for archivo in os.listdir(OUTPUT_DIR):
            if archivo.endswith(".jpg"):
                # Seguridad extra: no borrar la gráfica si Matplotlib la guardó en la misma carpeta
                if archivo != os.path.basename(ruta_grafica_final):
                    try:
                        os.remove(os.path.join(OUTPUT_DIR, archivo))
                        cantidad_borrada += 1
                    except Exception as e:
                        print(f"⚠️ No se pudo borrar {archivo}: {e}")
        print(f"✅ Limpieza completada. Se borraron {cantidad_borrada} frames temporales.")
    else:
        # 5. SI NO HAY GRÁFICA, RESCATAMOS LAS IMÁGENES
        print("⚠️ SEGURIDAD ACTIVADA: No se detectó la gráfica de ML.")
        print("📂 Se han conservado los frames JPG en la carpeta Assets para inspección manual.")
        veredicto = "Análisis Fallido - Revisar Terminal"


    # --- GUARDADO FINAL ---
    print("📝 Actualizando JSON final con la conclusión del ML...")
    with open(os.path.join(OUTPUT_DIR, "data_final.json"), "w", encoding='utf-8') as f:
        # Guardamos si hubo éxito o el error específico
        json.dump({"raw_data": datos_partida, "ml_decision": veredicto, "grafica_generada": se_genero_grafica}, f, indent=4)

    print(f"🏁 Proceso terminado. Veredicto Final: {veredicto}")
    return {"status": "ok" if se_genero_grafica else "error_ml", "veredicto": veredicto}
   

@app.post("/procesar-todo/")
async def endpoint_maestro(background_tasks: BackgroundTasks, ruta: str, tiempos: str = ""):
    if not os.path.exists(ruta):
        return {"error": "Ruta no encontrada"}
    
    lista_rangos = tiempos.split(",") if tiempos else []
    background_tasks.add_task(proceso_maestro_ysm, ruta, lista_rangos)
    return {"status": "Procesando", "vram_status": "GPU 1660 Super Activa"}


def preparar_data_para_ml(ruta_json):
    with open(ruta_json, "r") as f:
        datos = json.load(f)
    
    # Convertimos a DataFrame para manipularlo fácil
    df_lista = []
    for momento in datos:
        for det in momento['analisis']:
            df_lista.append({
                "momento": momento['frame'],
                "clase": det['objeto'],
                "valor_ocr": det['valor']
            })
    
    df = pd.DataFrame(df_lista)

    # --- LIMPIEZA PARA ML ---
    # Convertimos la columna 'valor' a números (ej: Vida, Munición)
    # Si Tesseract leyó "1OO" lo corregimos a "100"
    df['valor_limpio'] = pd.to_numeric(df['valor_ocr'].str.replace('O', '0'), errors='coerce').fillna(0)

    # --- MÉTRICAS PARA GRAFICAR ---
    # Contamos enemigos por cada frame (Esto es lo que el ML usará para predecir riesgo)
    conteo_enemigos = df[df['clase'] == 'person'].groupby('momento').count()['clase'].tolist()
    
    return {
        "x_ml": conteo_enemigos, # Datos de entrada para el modelo
        "y_grafica": conteo_enemigos, # Datos para Streamlit
        "status": "Data lista para Entrenamiento"
    }






