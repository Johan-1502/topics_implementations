**Documentación Técnica — ACO para TSP**

Resumen
-------
- Proyecto: Implementación de Algoritmo de Colonia de Hormigas (ACO) aplicado al Problema del Viajante (TSP).
- Objetivo: proporcionar una implementación didáctica y una interfaz interactiva para demostrar el comportamiento del ACO, permitiendo observar la evolución de feromonas, la selección de rutas y el efecto de los parámetros (alpha, beta, rho, Q, número de hormigas).

1. Objetivos técnicos
---------------------
- Implementar una versión funcional y clara de ACO para TSP con API reutilizable (`AntColony` en `src/aco.py`).
- Proveer utilidades para instancias (matriz de distancias Euclídeas y Haversine para coordenadas geográficas) en `src/tsp.py`.
- Crear ejemplos reproducibles (`examples/run_aco.py`, `examples/run_real.py`) y una GUI de escritorio (`app.py`) para visualización interactiva.
- Generar resultados y figuras exportables para la sustentación.

2. Descripción del algoritmo
----------------------------
El ACO es un metaheurístico inspirado en el comportamiento de búsqueda de rutas de las hormigas. Las hormigas construyen soluciones (tours) y depositan feromonas en los arcos que han usado. La probabilidad de que una hormiga elija el arco (i,j) viene dada por:

$P_{ij} = \dfrac{\tau_{ij}^{\alpha} \eta_{ij}^{\beta}}{\sum_{k \in allowed} \tau_{ik}^{\alpha} \eta_{ik}^{\beta}}$

donde:
- $\tau_{ij}$: nivel de feromona en el arco i->j.
- $\eta_{ij} = 1/d_{ij}$: información heurística (inversa de la distancia).
- $\alpha,\beta \ge 0$: parámetros que ponderan feromona y heurística.

Actualización de feromonas (evaporación + depósito):

$\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \sum_{k} \Delta\tau_{ij}^{k}$

con $\Delta\tau_{ij}^{k} = Q / L_{k}$ si la hormiga k utilizó el arco (i,j) en su tour, donde $L_k$ es la longitud de la ruta y $Q$ es una constante de escala.

3. Implementación — resumen de código
-------------------------------------
- `src/aco.py`:
  - Clase principal `AntColony` con constructor:
    - `AntColony(distances, n_ants=10, n_best=3, n_iterations=100, decay=0.5, alpha=1, beta=2, q=1.0)`
  - Métodos públicos:
    - `run(verbose=False)`: ejecuta el algoritmo completo (usa `step()` internamente).
    - `step()`: ejecuta una iteración (construcción de soluciones, evaporación y depósito de feromona) y actualiza el mejor global.
    - `reset()`: restaura feromonas y estado.
    - `get_state()`: devuelve dict con estado actual (`iteration`, `best_route`, `best_distance`, `pheromone`, `last_solutions`).
  - Lógica interna:
    - Construcción de rutas: probabilidad de transición basada en feromona^alpha * heurística^beta.
    - Depósito: las `n_best` mejores soluciones depositan `Q / distance` en sus arcos.

- `src/tsp.py`:
  - `coords_to_distance_matrix(coords)`: matriz Euclídea.
  - `haversine_distance_matrix(latlon_coords)`: matriz en km para lat/lon (Haversine).
  - `random_coords(n, seed, scale)`: genera coordenadas sintéticas.
  - `load_latlon_csv(path)`: carga CSV simple `name,lat,lon`.

- `examples/run_aco.py` y `examples/run_real.py`: scripts de ejemplo con visualización (matplotlib) y opción `--save`.

- `app.py`: GUI de escritorio en Tkinter. Controles disponibles:
  - Inicializar (aleatoria / ciudades reales), parámetros ACO (n_ants, n_best, n_iterations, decay, alpha, beta, Q).
  - Step, Run, Pausa/Resume, Reset, Guardar figuras.
  - Visualizaciones: gráfico de ruta (con flechas y etiquetas) y mapa de calor de feromonas (se actualiza in-place con `set_data`).

4. Interfaz y funcionamiento interactivo
--------------------------------------
- Uso recomendado para la sustentación:
  1. Inicializar con una instancia de ciudades reales (`data/spain_cities.csv`) o aleatoria.
  2. Presionar `Step` (varias veces) observando:
     - El log a la derecha: mejor distancia por iteración.
     - La matriz de feromona (mapa de calor): verás cómo algunas entradas se intensifican.
     - El gráfico superior: la mejor ruta encontrada (flechas para dirección).
  3. Usar `Run` para dejar converger (con `Delay` ajustable), pausar si se requiere inspeccionar un estado intermedio.
  4. Guardar figuras con `Guardar figuras` para incluir en la presentación.

5. Experimentos realizados (ejemplos)
-----------------------------------
- Instancia sintética: `examples/run_aco.py` con 12 ciudades aleatorias (seed=42). Parámetros de ejemplo: `n_ants=20`, `n_best=5`, `n_iterations=200`, `decay=0.3`, `alpha=1`, `beta=3`.
  - Resultado observado: convergencia a una solución de distancia ~297.25 (ver `outputs/route_*.png` si se han guardado).
- Instancia real (ciudades españolas): `examples/run_real.py` usa Haversine y la lista en `data/spain_cities.csv`. Resultado ejemplo: ruta total ≈ 5,040 km.

6. Validación y análisis
------------------------
- Comportamiento esperado:
  - Al principio las feromonas son uniformes; la heurística guía (1/d) la exploración.
  - Con iteraciones, los arcos frecuentes en buenas soluciones acumulan feromona; la probabilidad de selección de dichos arcos aumenta (explotación).
  - Parámetros:
    - Aumentar `alpha` incrementa la dependencia sobre la feromona (puede acelerar convergencia a soluciones subóptimas).
    - Aumentar `beta` favorece la heurística (distancias cortas) y puede ayudar a la exploración local.
    - Aumentar `decay` (rho) acelera la evaporación, lo que evita la fijación prematura.

- Métricas a reportar en la sustentación:
  - Mejor distancia por iteración (gráfico de convergencia).
  - Tiempos de cómputo (por iteración y total).
  - Comparación con heurística simple `nearest-neighbor` y mejora tras aplicar `2-opt` (recomendada como mejora).

7. Complejidad y rendimiento
----------------------------
- Construcción de soluciones: O(n_ants * n_cities^2) worst-case (por evaluación de probabilidades). Se puede optimizar con estructuras acumulativas o vectorización.
- Actualización de feromonas: O(n_best * n_cities) por iteración.
- Para N ciudades y A hormigas y T iteraciones, coste aproximado: O(T * A * N^2).

8. Reproducibilidad
-------------------
- Usar la semilla (`seed`) en los ejemplos para replicar coordenadas aleatorias.
- Guardar parámetros y logs (el GUI permite exportar imágenes; recomendamos también exportar CSV con el log, opción a implementar).

9. Estructura del repositorio (files relevantes)
----------------------------------------------
- `app.py` — GUI Tkinter (interactiva).
- `src/aco.py` — implementación ACO (clase `AntColony`).
- `src/tsp.py` — utilidades TSP y Haversine.
- `examples/run_aco.py` — runner de ejemplo (aleatorio).
- `examples/run_real.py` — runner con datos reales (Haversine).
- `data/spain_cities.csv` — conjunto de ejemplo de 12 ciudades españolas.
- `requerements.txt` — dependencias (`numpy`, `matplotlib`).

10. Limitaciones y mejoras futuras
---------------------------------
- Limitaciones actuales:
  - Implementación simple y didáctica, no optimizada para grandes instancias (1000+ ciudades).
  - Falta comparación automática con heurísticas (se puede añadir fácilmente).
  - No hay persistencia por defecto del log en CSV (se puede añadir botón "Export log").

- Mejoras recomendadas:
  - Añadir `nearest-neighbor` + `2-opt` y mostrar comparativa en la GUI.
  - Implementar vectorización/numba para acelerar cálculo de probabilidades y distancia.
  - Añadir monitor de arcos (serie temporal de feromona para un arco específico).
  - Añadir exportación CSV del log y opción para cargar CSV de ubicaciones personalizadas.

11. Cómo ejecutar
------------------
Desde PowerShell (en la carpeta del proyecto):

```powershell
python -m pip install -r requerements.txt
python app.py         # GUI de escritorio
python examples/run_aco.py --save   # ejemplo aleatorio y guardar figuras
python examples/run_real.py         # ejemplo con ciudades reales 
```
-----------------------------------------
- Probabilidad de transición (véase `transition_probabilities` en `src/aco.py`).
- Depósito de feromona (véase `_spread_pheromone` en `src/aco.py`).


