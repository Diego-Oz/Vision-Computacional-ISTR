import cv2
import os

# Ruta de los datos
dataPath = r'C:\Users\dortiz\Desktop\Vision-Computacional-main\ISTR'
imagePaths = os.listdir(dataPath)
print('Personas registradas:', imagePaths)

# Verificar si el modelo existe antes de cargarlo
modelo_path = r'C:\Users\dortiz\Desktop\Vision-Computacional-main\modeloLBPHFace.xml'

if not os.path.exists(modelo_path):
    print("ERROR: No se encontró el modelo entrenado.")
    exit()

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(modelo_path)

cap = cv2.VideoCapture(0)  # Para la cámara en vivo

if not cap.isOpened():
    print("ERROR: No se pudo abrir el video. Verifica la ruta.")
    exit()

# Cargar el clasificador de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video finalizado o no se puede leer.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    faces = faceClassif.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

    if len(faces) == 0:
        print("No se detectaron rostros en este fotograma.")

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        label_text = 'Desconocido'
        color = (0, 0, 255)

        if result[1] < 90:
            label_text = imagePaths[result[0]]
            color = (0, 255, 0)

        cv2.putText(frame, label_text, (x, y - 25), 2, 1.1, color, 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) == 27:  # Presiona ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
