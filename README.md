# 🌡️ Sistema de Control Difuso HVAC (Simulación)

Este proyecto implementa un controlador de temperatura basado en **Lógica Difusa (Fuzzy Logic)** tipo Mamdani, desarrollado como parte de la actividad de simulación de computadores.

El sistema incluye un **controlador predictivo (PD-Fuzzy)** capaz de anticipar cambios de temperatura basándose en la derivada del error (tasa de cambio), y una interfaz gráfica en tiempo real.

## 📋 Tabla de Contenidos
1. [Requisitos](#requisitos)
2. [Arquitectura](#arquitectura)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instalación y Ejecución](#instalación-y-ejecución)
5. [Validación Experimental](#validación-experimental)

---

## 🛠️ Requisitos
* **Node.js** (v14 o superior)
* **NPM** (Gestor de paquetes de Node)
* Navegador Web Moderno (Chrome, Firefox, Edge)

---

## 🏗️ Arquitectura

La solución sigue un patrón **MVC (Modelo-Vista-Controlador)** desacoplado:

1.  **Frontend (Vista):** HTML5/CSS3 + Vanilla JS. Utiliza `Chart.js` para renderizar las funciones de pertenencia dinámicas.
2.  **Backend (Controlador):** Servidor Express.js que expone una API REST (`POST /api/fuzzy/simulate`).
3.  **Fuzzy Engine (Modelo):** Lógica pura implementada manualmente (`src/logic/fuzzyEngine.js`). No utiliza librerías externas para la inferencia difusa.

---

## 📂 Estructura del Proyecto

El módulo se encuentra contenido en la carpeta `fuzzy_logic`:

```text
fuzzy_logic/
├── public/               # Archivos estáticos (Frontend)
│   ├── index.html        # Interfaz de usuario
│   ├── style.css         # Estilos Dashboard (Cyberpunk theme)
│   └── script.js         # Lógica cliente y comunicación API
├── src/                  # Código fuente del Backend
│   ├── controllers/      # Controladores de rutas
│   ├── logic/            # MOTOR DIFUSO (Fuzzificación, Reglas, Defuzzificación)
│   ├── routes/           # Definición de endpoints API
│   ├── tests/            # Pruebas automatizadas (Unit Testing)
│   └── index.js          # Punto de entrada del servidor
└── package.json          # Dependencias del proyecto
