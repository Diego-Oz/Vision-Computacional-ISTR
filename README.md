# 🧠 Vision-Computacional-ISTR

Este proyecto implementa un sistema de **reconocimiento facial y de gestos en tiempo real** utilizando Python y OpenCV. Fue desarrollado como parte de la materia **Software en Tiempo Real**, integrando conceptos clave como programación concurrente, sincronización, manejo de eventos y estructuras eficientes de procesamiento visual.

---

## 🎯 Problema abordado y solución

En entornos como seguridad, accesibilidad o interfaces sin contacto, se necesitan sistemas capaces de **reaccionar al instante** ante estímulos del entorno. Este sistema responde a ese reto mediante:

- Flujo sincronizado con reconocimiento facial y gestual.
- Manejo de eventos de usuario (`i` para capturar fondo, `ESC` para salir).
- Procesamiento eficiente de contornos para interpretar gestos.
- Registro de eventos con marcas de tiempo para auditoría.

---

## ⚙️ Características principales

- ✅ **Reconocimiento Facial en Vivo**: Detecta y reconoce rostros registrados desde la webcam.
- ✅ **Reconocimiento de Gestos**: Interpreta gestos de mano (0, 2, o 4+ dedos) en tiempo real.
- ✅ **Saludo Personalizado en Pantalla**: Muestra un mensaje al reconocer un rostro.
- ✅ **Registro de Eventos**: Guarda los reconocimientos en `registro_eventos.txt`.
- ✅ **Flujo en Tiempo Real**:
  - Programación orientada a eventos.
  - Procesamiento visual sin bloqueos.
  - Integración eficiente de estructuras y lógica reactiva.

---

## 🔧 Tecnologías utilizadas

- `Python 3.10+`
- `OpenCV (opencv-contrib-python)`
- `NumPy`
- `imutils`

---

## 📦 Instalación

```bash
# Clona el repositorio
https://github.com/Diego-Oz/Vision-Computacional-ISTR.git

# Instala las dependencias necesarias
pip install opencv-contrib-python numpy imutils



