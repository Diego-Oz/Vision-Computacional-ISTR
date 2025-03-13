# Vision-Computacional-ISTR
Este proyecto de Visión Computacional en Tiempo Real implementa reconocimiento facial y de gestos usando Python y OpenCV. Permite detectar y reconocer rostros previamente registrados, así como identificar gestos de la mano en tiempo real.

Este proyecto implementa **reconocimiento facial y de gestos** utilizando Python y OpenCV. Permite detectar rostros previamente registrados y reconocer gestos de la mano en **tiempo real**.

## Problema Abordado y Solución

En aplicaciones de seguridad, accesibilidad y control de interfaces, es crucial contar con sistemas que puedan identificar rostros y gestos de manera rápida y precisa. Sin embargo, el procesamiento en tiempo real enfrenta desafíos como la sincronización de tareas y la optimización del rendimiento.

Este proyecto resuelve estos problemas mediante la implementación de técnicas de programación concurrente, uso de semáforos para evitar bloqueos y una función recursiva para procesar los contornos de los gestos de manera eficiente. Gracias a estas mejoras, el sistema puede reconocer rostros y gestos en tiempo real sin interrupciones.

## Características  
✅ **Reconocimiento Facial**: Detecta y reconoce rostros en vivo o desde un video.

✅ **Reconocimiento de Gestos**: Identifica gestos de la mano y muestra un mensaje correspondiente.

✅ **Procesamiento en Tiempo Real**: Responde en milisegundos a la entrada de la cámara.

✅ **Optimización con OpenCV**: Uso de algoritmos eficientes para detección y clasificación.

✅ **Programación Concurrente**: Utiliza ThreadPoolExecutor para mejorar la ejecución en paralelo.

✅ **Uso de Semáforos**: Controla el acceso a la cámara para evitar bloqueos.

✅ **Procesamiento Recursivo de Contornos**: Filtra los contornos de manera eficiente para una detección más precisa.

## Instalación  
1. Clona este repositorio.  
2. Instala las dependencias necesarias:
  pip install opencv-contrib-python numpy imutils
3.  Ejecutar el reconocimiento facial:
   python ReconocimientoFacial.py
4. Ejecutar el reconocimiento de gestos:
   python ReconocimientoGestos.py

## Video Demostrativo
https://youtu.be/3TjLDaggnIM

