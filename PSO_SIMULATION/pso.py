from function import VectorResult, IFunction
import numpy as np
import random
import math
from default_values import w_max, w_min, c1 as c_1, c2 as c_2


class Particle:
    def __init__(self, pbest: np.ndarray, id: int):
        self.id: int = id
        self.pbest: np.ndarray = pbest
        self.position: np.ndarray = pbest
        self.iterations: list[ParticleIteration] = []
        self.current_value: float | None = None
        self.initialize_velocity()

    def initialize_velocity(self):
        velocity_vector = [0] * len(self.pbest)
        self.velocity: np.ndarray = np.array(velocity_vector)

    def save_iteration(self):
        particleIteration = ParticleIteration(self.pbest, self.position, self.velocity)
        self.iterations.append(particleIteration)


class PSO:

    def __init__(self, w: float | None = None, c1: float = c_1, c2: float = c_2):
        self.c1: float = c1
        self.c2: float = c2
        self.w: float | None = w
        self.gbest: np.ndarray|None = None
        self.best_value: float | None = None
        self.particles: list[Particle] = []
        self.iterations: list[Iteration] = []

    def update_inertia(self, current_iteration: int, quantity_of_iterations: int):
        self.w = w_max - (w_max - w_min) * (current_iteration / quantity_of_iterations)
        print("Actualizando inercia")

    def calculate_function(
        self,
        quantity_of_particles: int,
        quantity_of_iterations: int,
        function: IFunction,
        useConstrictionFactor: bool = False,
    ) -> np.ndarray | None:
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
        self.quantity_of_particles = quantity_of_particles
        self.quantity_of_iterations = quantity_of_iterations

    def define_gbest(self):
        best_value: float | None = self.best_value
        gbest: np.ndarray | None = self.gbest
        for i in range(len(self.particles)):
            particle = self.particles[i]
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
        inertia_component = particle.velocity * self.w
        r1 = random.random()
        r2 = random.random()
        cognitive_component = self.c1 * r1 * (particle.pbest - particle.position)
        social_component = self.c2 * r2 * (self.gbest - particle.position)
        new_velocity = inertia_component + cognitive_component + social_component
        # print(f"Partícula {particle.id}: \n - velocidad: {particle.velocity}\n - pbest: {particle.pbest}\n - position: {particle.position}\n - r1: {r1}\n - r2: {r2}\n - velocidad obtenida: {new_velocity}")

    def calculate_velocity_by_constriction(self, particle: Particle):
        r1 = random.random()
        r2 = random.random()
        phi = self.c1 + self.c2
        constrictionFactor = 2 / np.abs(2 - phi - math.sqrt(math.pow(phi, 2) - 4 * phi))
        cognitive_component = self.c1 * r1 * (particle.pbest - particle.position)
        social_component = self.c2 * r2 * (self.gbest - particle.position)
        new_velocity = constrictionFactor * (
            particle.velocity + cognitive_component + social_component
        )
        # print(f"Partícula {particle.id}: \n - velocidad: {particle.velocity}\n - pbest: {particle.pbest}\n - position: {particle.position}\n - r1: {r1}\n - r2: {r2}\n - velocidad obtenida: {new_velocity}")
        particle.velocity = new_velocity

    def update_position(self, particle: Particle):
        particle.position = particle.position + particle.velocity

    def update_pbest(self, particle: Particle, function: IFunction):
        new_value = self.executeFunctionValues(function, particle.position)

        if particle.current_value is not None and new_value < particle.current_value:
            particle.pbest = particle.position
            particle.current_value = new_value

    def executeFunctionValues(
        self, function: IFunction, variables: np.ndarray
    ) -> float:
        for i in range(function.vector_size):
            function.variables[i] = variables[i]
        return function.execute()

    def initialize_particles(self, quantityOfVariables: int, function: IFunction):
        for i in range(self.quantity_of_particles):
            particle = Particle(self.createRandomVector(quantityOfVariables), i)
            particle.current_value = self.executeFunctionValues(
                function, particle.pbest
            )
            print(f"pbest: {particle.pbest} - value {particle.current_value}")
            self.particles.append(particle)

    def createRandomVector(self, quantityOfVariables: int) -> np.ndarray:
        vector = []
        for i in range(quantityOfVariables):
            vector.append(random.uniform(0, 5))
        return np.array(vector)


class ParticleIteration:
    def __init__(self, pbest: np.ndarray, position: np.ndarray, velocity: np.ndarray):
        self.pbest: np.ndarray = trunc_vector(pbest)
        self.position: np.ndarray = trunc_vector(position)
        self.velocity: np.ndarray = trunc_vector(velocity)
        


class Iteration:

    def __init__(self):
        self.particles_iterations:list[ParticleIteration]=[]
        self.gbest:np.ndarray= np.array([])
        self.diversity: float = 0
        
    def add_particle_iteration(self, particle_iteration: ParticleIteration):
        self.particles_iterations.append(particle_iteration)
        
    def calculate_diversity(self):
        centroid = self.calculate_centroid()
        norm_sumatory:float = 0
        for particle in self.particles_iterations:
            norm_sumatory += float(np.linalg.norm(particle.position - centroid))
        diversity = norm_sumatory/len(self.particles_iterations)
        self.diversity = math.trunc(diversity * 10**5) / 10**5

    def calculate_centroid(self):
        sumatory:np.ndarray|None = None
        for particle in self.particles_iterations:
            if sumatory is not None:
                sumatory += particle.position
            else:
                sumatory = particle.position
        if sumatory is not None:
            return sumatory/len(self.particles_iterations)
        
    def set_gbest(self, gbest:np.ndarray):
        self.gbest = trunc_vector(gbest)
        

def trunc_vector(vector: np.ndarray):
    vector_to_return = []
    for i in range(len(vector)):
        vector_to_return.append(math.trunc(vector[i] * 10**5) / 10**5)
    return np.array(vector_to_return)