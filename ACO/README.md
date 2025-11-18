# ACO (Ant Colony Optimization) — Implementación para TSP

Resumen
-------
Proyecto con una implementación didáctica de Algoritmo de Colonia de Hormigas (ACO) aplicada al Problema del Viajante (TSP). Incluye:
- Código fuente (`src/`) con la clase `AntColony`.
- Ejemplos ejecutables (`examples/`).
- Interfaz de escritorio interactiva (`app.py`) para visualizar la evolución del algoritmo.
- Documentación técnica (`DOCUMENTACION_TECNICA.md`) y material de la sustentación (`Sustentación.pdf`).

Requisitos
----------
- Python 3.8+ (Windows).
- Dependencias: `numpy`, `matplotlib`.
- `tkinter` (incluido en la mayoría de distribuciones de Python en Windows).

Instalación
-----------
Desde la carpeta del proyecto:

```powershell
python -m pip install -r requerements.txt
```

Ejecución
---------
- Ejecutar la GUI interactiva (recomendado para la sustentación):

```powershell
python app.py
```

- Ejecutar ejemplos por consola:

```powershell
python examples/run_aco.py       # ejemplo aleatorio y visualización
python examples/run_aco.py --save  # guardar figuras en outputs/
python examples/run_real.py     # ejemplo con ciudades reales (Haversine)
```

Estructura del repositorio
---------------------------
- `app.py` — GUI Tkinter para control y visualización interactiva.
- `src/aco.py` — implementación de `AntColony` (métodos: `step`, `run`, `reset`, `get_state`).
- `src/tsp.py` — utilidades de instancias, Haversine y loader de CSV.
- `examples/` — scripts de ejemplo (`run_aco.py`, `run_real.py`).
- `data/spain_cities.csv` — ejemplo de 12 ciudades españolas para pruebas reales.
- `DOCUMENTACION_TECNICA.md` — documentación técnica para la entrega.
- `Sustentación.pdf` — material de presentación (adjunto).

Parámetros principales del ACO
-----------------------------
- `n_ants`: número de hormigas por iteración.
- `n_best`: cuántas hormigas depositan feromona.
- `n_iterations`: iteraciones totales.
- `decay` (rho): tasa de evaporación de feromonas.
- `alpha`, `beta`: pesos de feromona y heurística.

Interfaz — recomendaciones de uso
--------------------------------
1. Abrir `app.py` (GUI) y `Inicializar` una instancia (aleatoria o con `data/spain_cities.csv`).
2. Usar `Step` para avanzar iteraciones y observar:
   - El log (mejor por iteración).
   - La matriz de feromonas (mapa de calor que se actualiza en tiempo real).
   - El gráfico de la ruta (con flechas que indican el tour).
3. Usar `Run` con un `Delay` pequeño para observar la convergencia; usar `Pausa` para inspeccionar estados intermedios.
4. `Guardar figuras` para exportar imágenes que puedan incluirse en la presentación.

Documentación técnica
---------------------
Consulta `DOCUMENTACION_TECNICA.md` para la explicación detallada del algoritmo, métricas, complejidad, y ejemplos de ejecución.

