import cv2
import os
import imutils
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

BASE_DATA_PATH = os.path.join("data")

def capturar_rostros(nombre, ruta_video, ventana, label_progreso):
    person_path = os.path.join(BASE_DATA_PATH, nombre)

    if not os.path.exists(person_path):
        os.makedirs(person_path)
        try:
            print("Carpeta creada:", person_path)
        except UnicodeEncodeError:
            print("Carpeta creada:", person_path)

    cap = cv2.VideoCapture(ruta_video)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #######
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(person_path, f'rostro_{count}.jpg'), rostro)
            count += 1
            label_progreso.config(text=f"Rostros capturados: {count}")
            print(f"Rostro {count} capturado")

        cv2.imshow('Captura de rostros', frame)
        if cv2.waitKey(1) == 27 or count >= 300:
            break

    cap.release()
    cv2.destroyAllWindows()

    def finalizar():
        messagebox.showinfo("Finalizado", f"Se capturaron {count} rostros de {nombre}.")
        ventana.destroy()

    ventana.after(100, finalizar)

def seleccionar_video(entry_video):
    ruta = filedialog.askopenfilename(
        title="Selecciona un video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    if ruta:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, ruta)

def iniciar_captura(entry_nombre, entry_video, ventana, label_progreso):
    nombre = entry_nombre.get().strip()
    ruta_video = entry_video.get().strip()

    if not nombre or not ruta_video:
        messagebox.showwarning("Faltan datos", "Debes ingresar el nombre y seleccionar un video.")
        return

    hilo = threading.Thread(target=capturar_rostros, args=(nombre, ruta_video, ventana, label_progreso))
    hilo.start()

# === Interfaz Gráfica ===
ventana = tk.Tk()
ventana.title("Registro de Rostros")
ventana.geometry("500x300")
ventana.configure(bg="#f0f0f0")

tk.Label(ventana, text="Nombre de la persona:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack()

tk.Label(ventana, text="Ruta del video:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
entry_video = tk.Entry(ventana, width=40)
entry_video.pack()

btn_explorar = tk.Button(ventana, text="Seleccionar Video", command=lambda: seleccionar_video(entry_video))
btn_explorar.pack(pady=5)

label_progreso = tk.Label(ventana, text="Rostros capturados: 0", bg="#f0f0f0", font=("Arial", 12, "italic"))
label_progreso.pack(pady=10)

btn_iniciar = tk.Button(
    ventana,
    text="Iniciar Captura",
    command=lambda: iniciar_captura(entry_nombre, entry_video, ventana, label_progreso),
    bg="#c4f0c5"
)
btn_iniciar.pack(pady=20)

ventana.mainloop()
