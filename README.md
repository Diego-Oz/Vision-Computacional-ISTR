# 🧠 Vision-Computacional-ISTR

Sistema de **reconocimiento facial y de gestos en tiempo real** desarrollado con Python y OpenCV. Detecta y reconoce rostros previamente registrados e identifica gestos de la mano desde la webcam, sin latencia perceptible.

> Proyecto académico — Materia: Software en Tiempo Real | UNIBE

---

## 🎯 Problema abordado

En entornos de seguridad, accesibilidad e interfaces sin contacto se necesitan sistemas capaces de reaccionar al instante ante estímulos visuales. Este proyecto aborda ese reto implementando un pipeline de visión computacional con procesamiento concurrente y lógica reactiva.

---

## ✨ Características

- 👤 **Reconocimiento facial en vivo** — detecta y reconoce rostros registrados desde la webcam
- ✋ **Reconocimiento de gestos** — interpreta gestos de mano (0, 2 o 4+ dedos) en tiempo real
- 💬 **Saludo personalizado** — muestra mensaje en pantalla al identificar un rostro
- 📋 **Registro de eventos** — guarda cada reconocimiento con marca de tiempo en `registro_eventos.txt`
- ⚡ **Procesamiento sin bloqueos** — arquitectura orientada a eventos, sin interrupciones en el flujo visual

---

## 🛠 Stack

| Tecnología | Uso |
|-----------|-----|
| Python 3.10+ | Lenguaje principal |
| OpenCV (`opencv-contrib-python`) | Captura, procesamiento visual y reconocimiento |
| NumPy | Operaciones matriciales sobre frames |
| imutils | Utilidades de procesamiento de imagen |

---

## 🗂 Estructura del proyecto

entrenamiento/    → Scripts para registrar y entrenar rostros
reconocimiento/   → Lógica de reconocimiento facial y gestual
registro/         → Módulo de registro de eventos con timestamp
main.py           → Punto de entrada principal

---

## ⚙️ Conceptos técnicos aplicados

- Programación orientada a eventos para respuesta en tiempo real
- Sincronización de flujos visuales concurrentes
- Procesamiento de contornos para interpretación de gestos
- Estructuras de datos eficientes para clasificación de frames

---

## 📦 Instalación

```bash
git clone https://github.com/Diego-Oz/Vision-Computacional-ISTR.git
cd Vision-Computacional-ISTR
pip install -r requirements.txt
python main.py
```
