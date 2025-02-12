import cv2
import numpy as np
import imutils

# Iniciar cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
bg = None  # Fondo inicial

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo acceder a la cámara.")
        break

    frame = imutils.resize(frame, width=640)
    frame = cv2.flip(frame, 1)  # Espejo para que se vea natural
    frameAux = frame.copy()

    # Región de interés (ROI) para la detección de la mano
    ROI = frame[50:300, 380:600]
    cv2.rectangle(frame, (380, 50), (600, 300), (0, 255, 0), 2)

    if bg is not None:
        # Convertir a escala de grises y aplicar filtro para reducir ruido
        grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        grayROI = cv2.GaussianBlur(grayROI, (5, 5), 0)
        bgROI = bg[50:300, 380:600]

        # Diferencia entre el fondo y la mano
        dif = cv2.absdiff(grayROI, bgROI)
        _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
        th = cv2.medianBlur(th, 7)

        # Encontrar contornos
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]  # Tomar el contorno más grande

        for cnt in cnts:
            if cv2.contourArea(cnt) > 8000:  # Ajustar tamaño mínimo del contorno
                hull = cv2.convexHull(cnt, returnPoints=False)
                defects = cv2.convexityDefects(cnt, hull)

                fingers = 0  # Contador de dedos

                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])

                        # Calcular ángulo entre los dedos
                        a = np.linalg.norm(np.array(start) - np.array(far))
                        b = np.linalg.norm(np.array(end) - np.array(far))
                        c = np.linalg.norm(np.array(start) - np.array(end))
                        angle = np.degrees(np.arccos((a**2 + b**2 - c**2) / (2 * a * b)))

                        if angle <= 80:  # Si el ángulo es menor a 80º, contamos un dedo
                            fingers += 1
                            cv2.circle(ROI, far, 5, (255, 0, 0), -1)  # Punto azul en la unión de los dedos

                        # Dibujar líneas entre los dedos
                        cv2.line(ROI, start, far, (0, 255, 0), 2)
                        cv2.line(ROI, far, end, (0, 255, 0), 2)

                # Determinar el gesto basado en el número de dedos levantados
                message = "Desconocido"

                if fingers == 0:
                    message = "Ayudaaaaaa"
                elif fingers == 1:
                    message = "Profe, me esta viendo?"
                elif fingers == 2:
                    message = "To Chill"
                elif fingers == 3:
                    message = "OK"
                elif fingers >= 4:
                    message = "Hola caracola"

                # Mostrar el mensaje en la pantalla
                cv2.putText(frame, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.drawContours(ROI, [cnt], -1, (0, 0, 255), 2)  # Dibujar el contorno en rojo

        cv2.imshow('Threshold', th)

    # Mostrar la cámara
    cv2.imshow('Reconocimiento de Gestos', frame)

    # Controles
    k = cv2.waitKey(20)
    if k == ord('i'):
        bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
        print("Fondo capturado. Coloca tu mano en la región y muévela.")
    if k == 27:  # Presiona ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
