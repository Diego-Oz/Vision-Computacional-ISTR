import tkinter as tk
from tkinter import messagebox
import subprocess

def registrar_rostro():
    subprocess.run(["python", "registro/registro_rostro.py"])

def entrenar_modelo():
    subprocess.run(["python", "entrenamiento/entrenamiento_modelo.py"])

def ejecutar_reconocimiento():
    subprocess.Popen(["python", "reconocimiento/reconocimiento_completo.py"])

def salir():
    respuesta = messagebox.askyesno("Salir", "¿Estás seguro que deseas salir?")
    if respuesta:
        ventana.quit()

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Proyecto Visión Computacional")
ventana.geometry("400x300")
ventana.configure(bg="#f0f0f0")

# Título
titulo = tk.Label(ventana, text="Menú Principal", font=("Arial", 18, "bold"), bg="#f0f0f0")
titulo.pack(pady=20)

# Botones
boton1 = tk.Button(ventana, text="1. Registrar Rostro", command=registrar_rostro, width=30, height=2, bg="#e0e0e0")
boton1.pack(pady=5)

boton2 = tk.Button(ventana, text="2. Entrenar Modelo", command=entrenar_modelo, width=30, height=2, bg="#e0e0e0")
boton2.pack(pady=5)

boton3 = tk.Button(ventana, text="3. Ejecutar Reconocimiento", command=ejecutar_reconocimiento, width=30, height=2, bg="#e0e0e0")
boton3.pack(pady=5)

boton4 = tk.Button(ventana, text="Salir", command=salir, width=30, height=2, bg="#ffcccc")
boton4.pack(pady=20)

# Iniciar la interfaz
ventana.mainloop()
