import cv2
import os
import numpy as np

dataPath = '' #URL de la carpeta donde estan las imagenes (ISTR)
peopleList = os.listdir(dataPath)
print('Lista de personas:', peopleList)

labels = []
facesData = []
label = 0

# Leer imágenes de cada persona
for nameDir in peopleList:
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo imágenes de:', nameDir)

    for fileName in os.listdir(personPath):
        imagePath = os.path.join(personPath, fileName)
        image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            print(f"Error al cargar imagen: {imagePath}")
            continue

        facesData.append(image)
        labels.append(label)

    label += 1

# Asegurar que hay datos para entrenar
if len(facesData) == 0:
    print("Error: No hay imágenes para entrenar.")
    exit()

# Crear y entrenar el modelo LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
print("Entrenando modelo...")

face_recognizer.train(facesData, np.array(labels, dtype=np.int32))
face_recognizer.write('modeloLBPHFace.xml')

print("Modelo almacenado exitosamente.")
