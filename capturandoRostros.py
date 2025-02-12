import cv2
import os
import imutils

# Nombre de la persona que se quiere registrar
personName = 'Diego'
dataPath = ''#URL donde se va a almacenar los rostros
personPath = os.path.join(dataPath, personName)

# Crear la carpeta si no existe
if not os.path.exists(personPath):
    os.makedirs(personPath)
    print('Carpeta creada:', personPath)

# Capturar video
cap = cv2.VideoCapture#(URL donde se encuentra el video con el rostro)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el video o finalizó.")
        break

    # Corregir la orientación del video
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Redimensionar el video para mejor procesamiento
    frame = imutils.resize(frame, width=640)

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()

    # Detección de rostros (ajustamos valores para mejorar detección)
    faces = faceClassif.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # Dibujar rectángulo alrededor de la cara
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Extraer y guardar la imagen del rostro
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(personPath, f'rostro_{count}.jpg'), rostro)
        count += 1

    # Mostrar video con detección de rostros
    cv2.imshow('Frame', frame)

    # Condiciones de salida (ESC o capturar 300 imágenes)
    if cv2.waitKey(1) == 27 or count >= 300:
        break

cap.release()
cv2.destroyAllWindows()
