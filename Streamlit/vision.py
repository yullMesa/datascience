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