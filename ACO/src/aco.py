import numpy as np

class AntColony:
    """Algoritmo de colonia de hormigas (ACO) para el TSP.

    Esta implementación sigue las fórmulas típicas de ACO:

    - Probabilidad de transición desde i a j:
      $P_{ij} = \dfrac{\tau_{ij}^{\alpha} \eta_{ij}^{\beta}}{\sum_{k \in allowed} \tau_{ik}^{\alpha} \eta_{ik}^{\beta}}$
      donde $\eta_{ij} = 1/d_{ij}$ es la heurística (inversa de la distancia).

    - Actualización de feromona (evaporación + depósito):
      $\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \sum_{k} \Delta\tau_{ij}^{k}$
      con $\Delta\tau_{ij}^{k} = Q / L_{k}$ si la hormiga k usó el arco (i,j) en su ruta (L_k = longitud).

    Parámetros:
    - distances: matriz NxN de distancias (numpy array).
    - n_ants: número de hormigas por iteración.
    - n_best: número de mejores rutas que depositan feromona.
    - n_iterations: número de iteraciones.
    - decay: tasa de evaporación (rho).
    - alpha, beta: parámetros que ponderan feromona y heurística.
    - q: constante Q para el depósito de feromona (por defecto 1.0).
    """

    def __init__(self, distances, n_ants=10, n_best=3, n_iterations=100, decay=0.5, alpha=1, beta=2, q=1.0):
        self.distances = np.array(distances)
        n = len(self.distances)
        # inicializar feromonas uniformes
        self.pheromone = np.ones((n, n)) / n
        # guardar copia inicial para reset
        self._initial_pheromone = self.pheromone.copy()
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.q = q
        # estado del algoritmo (iteraciones, mejor solución)
        self.iteration = 0
        self.best_route = None
        self.best_distance = float('inf')
        self.last_solutions = []

    def _route_distance(self, route):
        distance = 0.0
        for i in range(len(route)):
            a = int(route[i])
            b = int(route[(i + 1) % len(route)])
            distance += float(self.distances[a, b])
        return distance

    def transition_probabilities(self, current, visited):
        """Devuelve el vector de probabilidades P_{current->j} sobre las ciudades no visitadas.

        Implementa directamente la fórmula de transición mencionada en la docstring.
        """
        n = len(self.distances)
        probs = np.zeros(n)
        for j in range(n):
            if j in visited:
                probs[j] = 0.0
            else:
                tau = self.pheromone[current, j] ** self.alpha
                eta = (1.0 / self.distances[current, j]) ** self.beta if self.distances[current, j] > 0 else 0.0
                probs[j] = tau * eta
        total = probs.sum()
        if total > 0:
            probs = probs / total
        return probs

    def _generate_route(self, start):
        route = [int(start)]
        visited = set(route)
        while len(route) < len(self.distances):
            current = route[-1]
            probs = self.transition_probabilities(current, visited)
            choices = [i for i in range(len(probs)) if i not in visited]
            if len(choices) == 0:
                break
            if probs.sum() == 0:
                next_city = int(np.random.choice(choices))
            else:
                next_city = int(np.random.choice(range(len(probs)), p=probs))
            route.append(next_city)
            visited.add(next_city)
        return route

    def _generate_solutions(self):
        solutions = []
        for _ in range(self.n_ants):
            start = np.random.randint(len(self.distances))
            route = self._generate_route(start)
            dist = self._route_distance(route)
            solutions.append((route, dist))
        return solutions

    def _spread_pheromone(self, solutions):
        # ordenar por mejor distancia (menor es mejor)
        sorted_solutions = sorted(solutions, key=lambda x: x[1])
        for route, dist in sorted_solutions[: self.n_best]:
            deposit = self.q / (dist + 1e-10)
            for i in range(len(route)):
                a = int(route[i])
                b = int(route[(i + 1) % len(route)])
                self.pheromone[a, b] += deposit

    def get_pheromone_matrix(self):
        return self.pheromone.copy()

    def run(self, verbose=False):
        # ejecutar varias iteraciones usando step() para mantener consistencia
        self.reset()
        best_route = None
        best_distance = float('inf')
        for iteration in range(self.n_iterations):
            it, bd = self.step()
            if verbose and (iteration % max(1, self.n_iterations // 10) == 0):
                print(f"Iter {iteration+1}/{self.n_iterations}: best distance {bd:.4f}")
        return self.best_route, self.best_distance

    def step(self):
        """Ejecuta una sola iteración del algoritmo.

        Devuelve (iteration, best_distance) tras la iteración.
        """
        solutions = self._generate_solutions()
        # evaporación
        self.pheromone = (1 - self.decay) * self.pheromone
        # depósito
        self._spread_pheromone(solutions)
        # actualizar mejor global
        iteration_best = min(solutions, key=lambda x: x[1])
        if iteration_best[1] < self.best_distance:
            self.best_route, self.best_distance = iteration_best[0], iteration_best[1]
        self.iteration += 1
        self.last_solutions = solutions
        return self.iteration, self.best_distance

    def reset(self):
        """Reinicia feromonas y estado del algoritmo al valor inicial."""
        self.pheromone = self._initial_pheromone.copy()
        self.iteration = 0
        self.best_route = None
        self.best_distance = float('inf')
        self.last_solutions = []

    def get_state(self):
        """Devuelve un dict con el estado actual útil para la interfaz."""
        return {
            'iteration': self.iteration,
            'best_route': [int(x) for x in self.best_route] if self.best_route is not None else None,
            'best_distance': float(self.best_distance) if self.best_distance != float('inf') else None,
            'pheromone': self.pheromone.copy(),
            'last_solutions': self.last_solutions,
        }
