# README --- Particle Swarm Optimization (PSO)

Este proyecto implementa el algoritmo **Particle Swarm Optimization
(PSO)** y varias funciones objetivo (Quadratic, Rosenbrock y
Rastrigin).\
Incluye además un sistema de iteraciones, diversidad y registro de
estados de cada partícula.

## 📌 Requisitos
Para la ejecución primero es necesario crear el entorno virtual con "python -m venv venv", luego ejecutar ".\venv\Scripts\activate" y finalmente "pip install -r requirements.txt" para instalar las liberías necesarias

Antes de ejecutar el programa, asegúrate de tener instalado:

-   **Python 3.10+**
-   Los siguientes módulos:

``` bash
pip install numpy
```

Si usas la interfaz gráfica con tkinter/ttkbootstrap, también instala:

``` bash
pip install ttkbootstrap
```

## 📁 Estructura del proyecto

    project/
    │
    ├── pso.py                     # Lógica principal del algoritmo PSO
    ├── function.py                # Definición de funciones objetivo
    ├── default_values.py          # Valores por defecto: w, c1, c2...
    ├── test.py                    # Archivo con pruebas del algoritmo
    ├── main.py                    # Programa principal (si existe interfaz gráfica)
    │
    └── README.md

## ▶️ Cómo ejecutar el programa

### 1. Ejecución del algoritmo PSO desde test.py

El archivo `test.py` incluye pruebas listas para ejecutarse.

Ejecuta:

``` bash
python test.py
```

Esto correrá:

-   PSO sobre funciones Quadratic, Rosenbrock y Rastrigin\
-   Mostrará resultados por consola\
-   Validará que pbest, gbest y movimientos estén funcionando
    correctamente

### 2. Si deseas ejecutar un archivo principal (ej. una GUI con tkinter)

Si tu proyecto incluye un `main.py`, entonces ejecuta:

``` bash
python main.py
```

## ⚙️ Cómo modificar parámetros

En `default_values.py` puedes cambiar:

``` python
w_max = 0.9
w_min = 0.4
c1 = 2.0
c2 = 2.0
```

Y en `test.py` puedes ajustar:

``` python
quantity_of_particles = 30
quantity_of_iterations = 100
func = QuadraticFunction(...)
```

## 🧪 Ejecutar pruebas adicionales

Si deseas ejecutar PSO en otra función:

``` python
from pso import PSO
from function import RastriginFunction

pso = PSO()
result = pso.calculate_function(
    quantity_of_particles=40,
    quantity_of_iterations=200,
    function=RastriginFunction(A=10, n=2)
)
print(result)
```

## 📌 Notas importantes

-   Todas las funciones objetivo implementan la interfaz `IFunction`.
-   Los vectores se normalizan a 5 decimales.
-   Se registra la diversidad poblacional en cada iteración.
-   Cada partícula conserva su historial completo.

