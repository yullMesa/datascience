# tkventana.py
import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta():
    """Abre una ventana de Windows para seleccionar una carpeta."""
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)  # Asegura que la ventana aparezca al frente
    ruta = filedialog.askdirectory()
    root.destroy()  # Cierra la instancia de tkinter para no dejar procesos colgados
    return ruta