"""
PSO (Particle Swarm Optimization) Implementation
------------------------------------------------
Este archivo contiene una implementación del algoritmo PSO con soporte para:
- Inercia variable
- Factor de constricción
- Registro de iteraciones y diversidad
- Evaluación mediante interfaz `IFunction`

Las clases principales son:
- Particle: Representa una partícula del enjambre
- PSO: Controla la ejecución del algoritmo
- ParticleIteration: Guarda el estado de una partícula en una iteración
- Iteration: Guarda el estado del enjambre en una iteración

Las funciones y métodos han sido documentados para facilitar su entendimiento.
"""

from function import VectorResult, IFunction
import numpy as np
import random
import math
from default_values import w_max, w_min, c1 as c_1, c2 as c_2


class Particle:
    """
    Representa una partícula dentro del enjambre PSO.

    Atributos:
        id (int): Identificador único de la partícula.
        pbest (np.ndarray): Mejor posición encontrada por la partícula.
        position (np.ndarray): Posición actual de la partícula.
        velocity (np.ndarray): Velocidad actual.
        iterations (list[ParticleIteration]): Historial por iteración.
        current_value (float | None): Valor actual evaluado por la función objetivo.
    """

    def __init__(self, pbest: np.ndarray, id: int):
        self.id: int = id
        self.pbest: np.ndarray = pbest
        self.position: np.ndarray = pbest
        self.iterations: list[ParticleIteration] = []
        self.current_value: float | None = None
        self.initialize_velocity()

    def initialize_velocity(self):
        """Inicializa la velocidad en un vector de ceros del tamaño del espacio de búsqueda."""
        velocity_vector = [0] * len(self.pbest)
        self.velocity: np.ndarray = np.array(velocity_vector)

    def save_iteration(self):
        """Guarda el estado actual de la partícula para la iteración actual."""
        particleIteration = ParticleIteration(self.pbest, self.position, self.velocity)
        self.iterations.append(particleIteration)


class PSO:
    """
    Implementación del algoritmo Particle Swarm Optimization.

    Parámetros:
        w (float | None): Factor de inercia.
        c1 (float): Peso cognitivo.
        c2 (float): Peso social.
    """

    def __init__(self, w: float | None = None, c1: float = c_1, c2: float = c_2):
        self.c1: float = c1
        self.c2: float = c2
        self.w: float | None = w
        self.gbest: np.ndarray | None = None
        self.best_value: float | None = None
        self.particles: list[Particle] = []
        self.iterations: list[Iteration] = []

    def update_inertia(self, current_iteration: int, quantity_of_iterations: int):
        """
        Actualiza dinámicamente la inercia según el progreso de iteraciones.
        """
        self.w = w_max - (w_max - w_min) * (current_iteration / quantity_of_iterations)
        print("Actualizando inercia")

    def calculate_function(
        self,
        quantity_of_particles: int,
        quantity_of_iterations: int,
        function: IFunction,
        useConstrictionFactor: bool = False,
    ) -> np.ndarray | None:
        """
        Ejecuta el algoritmo PSO completo.

        Args:
            quantity_of_particles (int): Número de partículas.
            quantity_of_iterations (int): Número de iteraciones.
            function (IFunction): Función objetivo.
            useConstrictionFactor (bool): Si se usa el factor de constricción.

        Returns:
            np.ndarray | None: Mejor solución encontrada (gbest).
        """
        self.set_parameters(quantity_of_particles, quantity_of_iterations)
        self.initialize_particles(function.vector_size, function)
        self.define_gbest()

        print(
            f"Información relevante: \n - c1: {self.c1}\n - c2: {self.c2}\n - gbest: {self.gbest}\n"
        )

        for i in range(self.quantity_of_iterations):
            iteration = Iteration()

            for particle in self.particles:
                if useConstrictionFactor:
                    self.calculate_velocity_by_constriction(particle)
                else:
                    self.update_inertia(i, quantity_of_iterations)
                    self.calculate_velocity_by_inertia(particle)

                self.update_position(particle)
                self.update_pbest(particle, function)
                particle.save_iteration()
                iteration.add_particle_iteration(particle.iterations[i])

            self.define_gbest()
            if self.gbest is not None:
                iteration.set_gbest(self.gbest)
            iteration.calculate_diversity()
            self.iterations.append(iteration)

        print(f"Mejor valor encontrado: {self.gbest}")
        return self.gbest

    def set_parameters(self, quantity_of_particles: int, quantity_of_iterations: int):
        """Guarda los parámetros básicos del algoritmo."""
        self.quantity_of_particles = quantity_of_particles
        self.quantity_of_iterations = quantity_of_iterations

    def define_gbest(self):
        """
        Busca entre todas las partículas el mejor valor global.
        """
        best_value: float | None = self.best_value
        gbest: np.ndarray | None = self.gbest

        for particle in self.particles:
            if gbest is not None:
                if (
                    particle.current_value is not None
                    and best_value is not None
                    and particle.current_value < best_value
                ):
                    gbest = particle.pbest
                    best_value = particle.current_value
            else:
                gbest = particle.pbest
                best_value = particle.current_value

        self.gbest = gbest
        self.best_value = best_value

    def calculate_velocity_by_inertia(self, particle: Particle):
        """Calcula la nueva velocidad usando la fórmula con inercia variable."""
        inertia_component = particle.velocity * self.w
        r1 = random.random()
        r2 = random.random()

        cognitive_component = self.c1 * r1 * (particle.pbest - particle.position)
        social_component = self.c2 * r2 * (self.gbest - particle.position)

        new_velocity = inertia_component + cognitive_component + social_component
        particle.velocity = new_velocity

    def calculate_velocity_by_constriction(self, particle: Particle):
        """Calcula la velocidad aplicando un factor de constricción (Clerc)."""
        r1 = random.random()
        r2 = random.random()
        phi = self.c1 + self.c2

        constrictionFactor = 2 / np.abs(2 - phi - math.sqrt(phi**2 - 4 * phi))

        cognitive_component = self.c1 * r1 * (particle.pbest - particle.position)
        social_component = self.c2 * r2 * (self.gbest - particle.position)

        new_velocity = constrictionFactor * (
            particle.velocity + cognitive_component + social_component
        )
        particle.velocity = new_velocity

    def update_position(self, particle: Particle):
        """Actualiza la posición de la partícula."""
        particle.position = particle.position + particle.velocity

    def update_pbest(self, particle: Particle, function: IFunction):
        """
        Actualiza pbest si la nueva posición es mejor.
        """
        new_value = self.executeFunctionValues(function, particle.position)

        if particle.current_value is not None and new_value < particle.current_value:
            particle.pbest = particle.position
            particle.current_value = new_value

    def executeFunctionValues(
        self, function: IFunction, variables: np.ndarray
    ) -> float:
        """Ejecuta la función objetivo con las variables dadas."""
        for i in range(function.vector_size):
            function.variables[i] = variables[i]
        return function.execute()

    def initialize_particles(self, quantityOfVariables: int, function: IFunction):
        """Crea partículas iniciales con posiciones aleatorias."""
        for i in range(self.quantity_of_particles):
            particle = Particle(self.createRandomVector(quantityOfVariables), i)
            particle.current_value = self.executeFunctionValues(
                function, particle.pbest
            )
            print(f"pbest: {particle.pbest} - value {particle.current_value}")
            self.particles.append(particle)

    def createRandomVector(self, quantityOfVariables: int) -> np.ndarray:
        """Crea un vector aleatorio dentro del rango [0, 5]."""
        return np.array([random.uniform(0, 5) for _ in range(quantityOfVariables)])


class ParticleIteration:
    """Guarda el estado truncado de una partícula en una iteración."""

    def __init__(self, pbest: np.ndarray, position: np.ndarray, velocity: np.ndarray):
        self.pbest: np.ndarray = trunc_vector(pbest)
        self.position: np.ndarray = trunc_vector(position)
        self.velocity: np.ndarray = trunc_vector(velocity)


class Iteration:
    """Representa una iteración completa del enjambre."""

    def __init__(self):
        self.particles_iterations: list[ParticleIteration] = []
        self.gbest: np.ndarray = np.array([])
        self.diversity: float = 0

    def add_particle_iteration(self, particle_iteration: ParticleIteration):
        """Añade el estado de una partícula en esta iteración."""
        self.particles_iterations.append(particle_iteration)

    def calculate_diversity(self):
        """Calcula la diversidad del enjambre mediante la distancia al centroide."""
        centroid = self.calculate_centroid()
        norm_sumatory: float = sum(
            float(np.linalg.norm(p.position - centroid))
            for p in self.particles_iterations
        )
        diversity = norm_sumatory / len(self.particles_iterations)
        self.diversity = math.trunc(diversity * 10**5) / 10**5

    def calculate_centroid(self):
        """Calcula el centroide de las posiciones de las partículas."""
        if not self.particles_iterations:
            return None
        sumatory = sum((p.position for p in self.particles_iterations))
        return sumatory / len(self.particles_iterations)

    def set_gbest(self, gbest: np.ndarray):
        """Guarda el gbest truncado para esta iteración."""
        self.gbest = trunc_vector(gbest)


def trunc_vector(vector: np.ndarray):
    """Trunca un vector a 5 decimales."""
    return np.array([math.trunc(v * 10**5) / 10**5 for v in vector])
