import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Ruta base de datos
DATA_PATH = os.path.join("data")
MODEL_PATH = os.path.join("modeloLBPHFace.xml")

def entrenar_modelo(label_estado):
    peopleList = os.listdir(DATA_PATH)
    labels = []
    facesData = []
    label = 0

    if not peopleList:
        messagebox.showerror("Error", "No hay carpetas de personas en la carpeta 'data'.")
        return

    for nameDir in peopleList:
        personPath = os.path.join(DATA_PATH, nameDir)
        if not os.path.isdir(personPath):
            continue

        for fileName in os.listdir(personPath):
            imagePath = os.path.join(personPath, fileName)
            image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

            if image is None:
                continue

            facesData.append(image)
            labels.append(label)
        label += 1

    if len(facesData) == 0:
        messagebox.showerror("Error", "No se encontraron imágenes válidas para entrenar.")
        return

    label_estado.config(text="Entrenando modelo...")
    ventana.update()

    try:
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(facesData, np.array(labels, dtype=np.int32))
        face_recognizer.write(MODEL_PATH)
        label_estado.config(text="Entrenamiento completado. Modelo guardado.")
        messagebox.showinfo("Éxito", f"Modelo entrenado con {len(set(labels))} persona(s).")
    except Exception as e:
        label_estado.config(text="Error durante el entrenamiento.")
        messagebox.showerror("Error", str(e))

# === Interfaz Gráfica ===
ventana = tk.Tk()
ventana.title("Entrenamiento del Modelo")
ventana.geometry("400x200")
ventana.configure(bg="#f0f0f0")

tk.Label(ventana, text="Entrenamiento del Reconocedor Facial", bg="#f0f0f0", font=("Arial", 14)).pack(pady=15)

label_estado = tk.Label(ventana, text="Estado: esperando acción", bg="#f0f0f0", font=("Arial", 10, "italic"))
label_estado.pack(pady=10)

def confirmar_entrenamiento():
    if os.path.exists(MODEL_PATH):
        respuesta = messagebox.askyesno("Advertencia", "Ya existe un modelo entrenado. ¿Deseas reemplazarlo?")
        if not respuesta:
            return
    entrenar_modelo(label_estado)

btn_entrenar = tk.Button(ventana, text="Entrenar Modelo", command=confirmar_entrenamiento, width=25, height=2, bg="#d0f0d0")
btn_entrenar.pack(pady=15)

ventana.mainloop()
