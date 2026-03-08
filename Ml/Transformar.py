import matplotlib.pyplot as plt
import os

def analizar_y_graficar(datos_json):

    
    # 1. Extraer datos para el análisis
    ejes_x = [] 
    ejes_y = [] 
    
    for i, frame in enumerate(datos_json):
        ejes_x.append(f"F{i}")
        # Contamos enemigos como métrica principal
        enemigos = sum(1 for obj in frame.get('analisis', []) if obj.get('objeto') == 'person')
        ejes_y.append(enemigos)
    
    # 2. LÓGICA DEL ML (La conclusión)
    max_enemigos = max(ejes_y) if ejes_y else 0
    if max_enemigos > 5:
        conclusion = "PELIGRO CRÍTICO: Emboscada detectada"
    elif max_enemigos > 2:
        conclusion = "RIESGO MODERADO: Presencia enemiga"
    else:
        conclusion = "ZONA SEGURA: Sin amenazas"
    
    # 3. Crear la Gráfica
    plt.figure(figsize=(8, 4))
    plt.plot(ejes_x, ejes_y, marker='o', color='#00FFCC', linestyle='-', linewidth=2)
    plt.fill_between(ejes_x, ejes_y, color='#00FFCC', alpha=0.2) # Toque estético
    plt.title("Análisis Forense: Intensidad de Amenazas")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 4. GUARDAR (Asegúrate de que la ruta sea Streamlit/Assets)
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_grafica = os.path.join(ruta_base, "Streamlit", "Assets", "grafica_ml.png")
    
    # ... código de tu gráfica ...
    plt.savefig(ruta_grafica)
    plt.clf()   # Limpia la figura actual
    plt.close('all') # Cierra todas las ventanas de Matplotlib abiertas
    
    # Liberar memoria explícitamente para el ML
    import gc
    gc.collect() 
    
    return conclusion, ruta_grafica