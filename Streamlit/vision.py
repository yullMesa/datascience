import pytesseract
from PIL import Image
import os

# Configuramos la ruta al ejecutable que tienes en tu proyecto
pytesseract.pytesseract.tesseract_cmd = r'teser\tesseract.exe'

def procesar_frame_a_frame(ruta_carpeta):
    datos_partida = []
    
    if not os.path.exists(ruta_carpeta):
        return "Error: La carpeta de frames no existe."
    
    lista_imagenes = [f for f in os.listdir(ruta_carpeta) if f.endswith(('.png', '.jpg'))]
    lista_imagenes.sort() # Para leerlos en orden cronológico
    
    for frame in lista_imagenes:
        img = Image.open(os.path.join(ruta_carpeta, frame))
        
        # Aquí definimos el área de interés (ROI)
        # Ejemplo: (izquierda, arriba, derecha, abajo) 
        # Tienes que ajustar estos números según tu resolución
        area_vida = (100, 900, 400, 950) 
        recorte = img.crop(area_vida)
        
        # Extraemos el texto
        texto = pytesseract.image_to_string(recorte, config='--psm 7 digits')
        
        datos_partida.append({"frame": frame, "valor": texto.strip()})
        print(f"Procesado {frame}: {texto.strip()}")
        
    return datos_partida