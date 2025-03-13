import cv2
import numpy as np
import imutils
import threading
import time
from threading import Semaphore

# Control de acceso
semaforo_gestos = Semaphore(1)

def reconocimiento_gestos():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("No se pudo acceder a la cámara.")
        
        bg = None
        
        while True:
            try:
                semaforo_gestos.acquire()
                ret, frame = cap.read()
                semaforo_gestos.release()
                
                if not ret:
                    raise Exception("Error al leer el fotograma de la cámara.")
                
                frame = imutils.resize(frame, width=640)
                frame = cv2.flip(frame, 1)
                frameAux = frame.copy()
                ROI = frame[50:300, 380:600]
                cv2.rectangle(frame, (380, 50), (600, 300), (0, 255, 0), 2)
                
                if bg is not None:
                    grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
                    dif = cv2.absdiff(grayROI, bg[50:300, 380:600])
                    _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
                    th = cv2.medianBlur(th, 7)
                    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
                    
                    for cnt in cnts:
                        if cv2.contourArea(cnt) > 8000:
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
                            message = "Desconocido"
                            if fingers == 0:
                                message = "Ey Profe!"
                            elif fingers == 2:
                                message = "VAMO ALLA"
                            elif fingers >= 4:
                                message = "UNIBE"
                            cv2.putText(frame, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2, cv2.LINE_AA)
                            cv2.drawContours(ROI, [cnt], -1, (0, 0, 255), 2)
                    
                    cv2.imshow('Threshold', th)
                
                cv2.imshow('Reconocimiento de Gestos', frame)
                k = cv2.waitKey(20)
                if k == ord('i'):
                    bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
                    print("Fondo capturado. Coloca tu mano en la región y muévela.")
                if k == 27:
                    break
            except Exception as e:
                print(f"Error en el procesamiento de gestos: {e}")
                break
        
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error al iniciar el reconocimiento de gestos: {e}")

# Ejecutar
task_gestos = threading.Thread(target=reconocimiento_gestos)
task_gestos.start()
task_gestos.join()
