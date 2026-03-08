import os
import cv2
import pytesseract
import numpy as np

def localizar_y_leer_dato(img_frame, ruta_icono_referencia):
    # 1. Cargamos el frame y el icono que buscamos (ej: el logo de $ del juego)
    img_gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(ruta_icono_referencia, 0)
    w, h = template.shape[::-1]

    # 2. Buscamos el icono en todo el frame
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Si la coincidencia es alta (ej: > 80%), encontramos la UI
    if max_val > 0.8:
        # Definimos el área de lectura a la derecha del icono encontrado
        x_inicio = max_loc[0] + w
        y_inicio = max_loc[1]
        # Recortamos un rectángulo de 150x50 píxeles al lado del icono
        roi = img_frame[y_inicio:y_inicio+h, x_inicio:x_inicio+150]
        
        # Limpiamos para Tesseract
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(roi_gray, 180, 255, cv2.THRESH_BINARY_INV)
        
        dato = pytesseract.image_to_string(thresh, config='--psm 7')
        return dato.strip()
    
    return None

def escanear_con_ancla(ruta_frames, ruta_icono):
    # Cargamos el "molde" (el PNG que creaste)
    icono = cv2.imread(ruta_icono, 0) # Cargamos en gris
    if icono is None:
        return "Error: No se encontró el archivo PNG del icono."

    w, h = icono.shape[::-1]
    resultados = []

    for archivo in os.listdir(ruta_frames):
        img_bgr = cv2.imread(os.path.join(ruta_frames, archivo))
        if img_bgr is None: continue
        
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # Buscamos el icono en el frame
        res = cv2.matchTemplate(img_gray, icono, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # Si la coincidencia es mayor al 80%
        if max_val > 0.8:
            # Definimos la zona de lectura (ROI) justo a la derecha del icono
            x, y = max_loc
            # Ajustamos el cuadro: x + ancho del icono, mismo y, 150px de largo
            roi = img_bgr[y:y+h, x+w : x+w+150] 

            # Pre-procesar el recorte para Tesseract
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(roi_gray, 150, 255, cv2.THRESH_BINARY_INV)

            # Tesseract lee el recorte
            texto = pytesseract.image_to_string(thresh, config='--psm 7')
            resultados.append(f"En {archivo}: {texto.strip()}")

    return resultados