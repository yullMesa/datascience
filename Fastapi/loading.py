from fastapi import FastAPI, BackgroundTasks
import cv2
import os

app = FastAPI()

# Mantenemos tu ruta de Assets de Streamlit para los frames
OUTPUT_DIR = os.path.join("..", "Streamlit", "Assets", "frames_extraidos")

def extraer_momentos_especificos(video_path, rangos):
    cap = cv2.VideoCapture(video_path) # OpenCV lo abre directamente del disco
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    for r in rangos:
        inicio, fin = map(int, r.split('-'))
        frame_actual = int(inicio * fps)
        frame_limite = int(fin * fps)
        salto = int(fps * 7) # Tu regla de los 7 segundos
        
        while frame_actual <= frame_limite:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_actual)
            ret, frame = cap.read()
            if not ret: break
            
            nombre = f"moment_{frame_actual}.jpg"
            cv2.imwrite(os.path.join(OUTPUT_DIR, nombre), frame)
            frame_actual += salto
            
    cap.release()

@app.post("/procesar-local/")
async def procesar(background_tasks: BackgroundTasks, ruta: str, tiempos: str = ""):
    # Verificamos que la ruta que el usuario pegó sea real
    if not os.path.exists(ruta):
        return {"error": "No se encontró el archivo en la ruta especificada"}
        
    lista_rangos = tiempos.split(",") if tiempos else []
    
    # Ejecutamos la tarea pesada en el fondo
    background_tasks.add_task(extraer_momentos_especificos, ruta, lista_rangos)
    
    return {"status": "Leyendo archivo directamente del disco", "path": ruta}