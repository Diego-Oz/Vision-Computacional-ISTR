import cv2
import numpy as np
import imutils
import os
from datetime import datetime

# === Configuración inicial ===
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model_path = "modeloLBPHFace.xml"
data_path = "data"

print("Inicializando reconocimiento...")

# === Verificar modelo ===
try:
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
except Exception as e:
    print("ERROR: No se pudo cargar el modelo:", e)
    exit()

# === Obtener nombres entrenados ===
try:
    nombres = os.listdir(data_path)
except Exception as e:
    print("ERROR: No se pudieron cargar los nombres:", e)
    nombres = []

# === Logging ===
def registrar_evento(mensaje):
    with open("registro_eventos.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")

# === Inicializar cámara ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara.")
    exit()

# === Variables de control ===
nombre_reconocido = None
saludo_mostrado = False
bg = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = imutils.resize(frame, width=640)
    frame = cv2.flip(frame, 1)
    frame_aux = frame.copy()

    # Reconocimiento facial
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        if result[1] < 90 and result[0] < len(nombres):
            nombre_reconocido = nombres[result[0]]
            color = (0, 255, 0)
            saludo_texto = f"Hola {nombre_reconocido}, presiona la tecla 'i' para analizar tus gestos"
            if not saludo_mostrado:
                registrar_evento(f"Reconocimiento facial exitoso: {nombre_reconocido}")
                saludo_mostrado = True
        else:
            nombre_reconocido = "Desconocido"
            saludo_texto = "Rostro no reconocido"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, nombre_reconocido, (x, y - 10), 2, 0.8, color, 2, cv2.LINE_AA)

    if saludo_mostrado:
        cv2.putText(frame, saludo_texto, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # === Reconocimiento de gestos con tecla 'i'
    ROI = frame[50:300, 380:600]
    cv2.rectangle(frame, (380, 50), (600, 300), (0, 255, 0), 2)

    if bg is not None:
        grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        dif = cv2.absdiff(grayROI, bg[50:300, 380:600])
        _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
        th = cv2.medianBlur(th, 7)
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in cnts:
            if cv2.contourArea(cnt) < 8000:
                continue

            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)
            fingers = 0
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    a = np.linalg.norm(np.array(start) - np.array(far))
                    b = np.linalg.norm(np.array(end) - np.array(far))
                    c = np.linalg.norm(np.array(start) - np.array(end))
                    angle = np.degrees(np.arccos((a**2 + b**2 - c**2) / (2 * a * b)))
                    if angle <= 80:
                        fingers += 1

            mensaje = "Desconocido"
            if fingers == 0:
                mensaje = "AYUDA"
            elif fingers == 2:
                mensaje = "FELIZ SEMANA SANTA"
            elif fingers >= 4:
                mensaje = "UNIVERSIDAD IBEROAMERICANA"

            cv2.putText(frame, mensaje, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
            registrar_evento(f"Gesto detectado de {nombre_reconocido or 'Desconocido'}: {mensaje}")

        cv2.imshow('Threshold', th)

    cv2.imshow("Reconocimiento Facial + Gestos", frame)

    key = cv2.waitKey(1)
    if key == ord('i'):
        bg = cv2.cvtColor(frame_aux, cv2.COLOR_BGR2GRAY)
        print("Fondo capturado. Puedes mover la mano en el área verde.")
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
