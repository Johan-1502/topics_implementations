"""
Módulo de funciones objetivo para PSO
--------------------------------------
Este archivo define una interfaz abstracta `IFunction` y varias implementaciones
concretas (funciones cuadrática, Rosenbrock, y Rastrigin), además de utilidades
como `Variable`, `BoundedVariable` y `VectorResult`.

Las clases poseen documentación detallada para facilitar su comprensión.
"""

from abc import ABC, abstractmethod
import math
import numpy as np


class IFunction(ABC):
    """
    Interfaz abstracta que representa una función objetivo para algoritmos de optimización.

    Una implementación de esta interfaz debe definir:
    - El tamaño del vector (`vector_size`)
    - Una lista de variables (`variables`)
    - Un método de ejecución (`execute`) que calcule el valor de la función
    - Métodos para inicializar y obtener el vector de variables
    """

    @property
    @abstractmethod
    def vector_size(self) -> int:
        """Cantidad de variables que componen el vector de entrada."""
        pass

    @vector_size.setter
    @abstractmethod
    def vector_size(self, val):
        """Asigna el tamaño del vector de variables."""
        pass

    @property
    @abstractmethod
    def variables(self) -> list[float]:
        """Lista de valores numéricos que representan las variables del modelo."""
        pass

    @variables.setter
    @abstractmethod
    def variables(self, val):
        """Define la lista de variables que serán usadas por la función objetivo."""
        pass

    @abstractmethod
    def execute(self) -> float:
        """Ejecuta la función objetivo con los valores actuales del vector y retorna su resultado."""
        pass

    @abstractmethod
    def obtain_array_vector(self) -> list[float]:
        """Retorna un vector del mismo tamaño que `variables`, inicializado en ceros."""
        pass

    @abstractmethod
    def initialize_vector(self):
        """Inicializa `variables` con valores por defecto (generalmente ceros)."""
        pass


class Variable:
    """
    Representa una variable numérica genérica.

    Args:
        value (float): Valor numérico de la variable.
    """

    def __init__(self, value: float):
        self.value: float = value


class QuadraticFunction(IFunction):
    """
    Función cuadrática bidimensional de la forma:

        f(x, y) = a(x - b)^2 + c(y - d)^2

    Comúnmente usada por su simplicidad y forma parabólica.
    """

    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.variables = []
        self.vector_size = 2
        self.initialize_vector()

    @property
    def vector_size(self) -> int:
        return self._vector_size

    @vector_size.setter
    def vector_size(self, val):
        self._vector_size = val

    @property
    def variables(self) -> list[float]:
        return self._variables

    @variables.setter
    def variables(self, val):
        self._variables = val

    def initialize_vector(self):
        """Inicializa el vector con ceros según `vector_size`."""
        for _ in range(self.vector_size):
            self.variables.append(0)

    def execute(self) -> float:
        """Evalúa la función cuadrática en los valores actuales de `variables`."""
        x = self.variables[0]
        y = self.variables[1]
        return self.a * (x - self.b) ** 2 + self.c * (y - self.d) ** 2

    def add_variable(self, variable: float):
        """Agrega una variable adicional (no utilizada en esta función)."""
        self.variables.append(variable)

    def obtain_array_vector(self) -> list[float]:
        """Retorna un vector de ceros del tamaño actual de `variables`."""
        return [0 for _ in self.variables]


class RosenbrockFunction(IFunction):
    """
    Función de Rosenbrock en dos dimensiones:

        f(x, y) = a(b - x)^2 + (y - x^2)^2

    Es una función no convexa clásica usada para pruebas de optimización.
    """

    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self.variables = []
        self.vector_size = 2
        self.initialize_vector()

    @property
    def vector_size(self) -> int:
        return self._vector_size

    @vector_size.setter
    def vector_size(self, val):
        self._vector_size = val

    @property
    def variables(self) -> list[float]:
        return self._variables

    @variables.setter
    def variables(self, val):
        self._variables = val

    def initialize_vector(self):
        """Inicializa el vector con valores cero."""
        for _ in range(self.vector_size):
            self.variables.append(0)

    def execute(self) -> float:
        """Evalúa la función de Rosenbrock."""
        x = self.variables[0]
        y = self.variables[1]
        return self.a * (self.b - x) ** 2 + (y - x ** 2) ** 2

    def add_variable(self, variable: float):
        self.variables.append(variable)

    def obtain_array_vector(self) -> list[float]:
        return [0 for _ in self.variables]


class RastriginFunction(IFunction):
    """
    Función de Rastrigin n-dimensional:

        f(x) = A*n + Σ[x_i^2 - A*cos(2πx_i)]

    Es altamente multimodal, ideal para evaluar exploración de PSO.
    """

    def __init__(self, A: float, n: int):
        self.A = A
        self.n = n
        self.variables = []
        self.vector_size = n
        self.initialize_vector()

    @property
    def vector_size(self) -> int:
        return self._vector_size

    @vector_size.setter
    def vector_size(self, val):
        self._vector_size = val

    @property
    def variables(self) -> list[float]:
        return self._variables

    @variables.setter
    def variables(self, val):
        self._variables = val

    def initialize_vector(self):
        """Inicializa el vector con valores cero."""
        for _ in range(self.vector_size):
            self.variables.append(0)

    def execute(self) -> float:
        """Evalúa la función de Rastrigin."""
        sumatory = 0
        for i in range(self.n):
            x_i = self.variables[i]
            sumatory += x_i ** 2 - self.A * math.cos(2 * math.pi * x_i)
        return self.A * self.n + sumatory

    def add_variable(self, variable: float):
        self.variables.append(variable)

    def obtain_array_vector(self) -> list[float]:
        return [0 for _ in self.variables]


class BoundedVariable(Variable):
    """
    Variable con límites numéricos.

    Args:
        value (float): Valor de la variable.
        min_value (float): Límite inferior permitido.
        max_value (float): Límite superior permitido.
    """

    def __init__(self, value: float, min_value: float, max_value: float):
        super().__init__(value)
        self.min_value = min_value
        self.max_value = max_value

    def isValidValue(self, value: float) -> bool:
        """Retorna True si `value` está dentro de los límites establecidos."""
        return self.min_value <= value <= self.max_value


class VectorResult:
    """
    Contenedor para almacenar resultados de funciones objetivo.

    Args:
        size (int): Número máximo de variables aceptadas.
        function (IFunction): Función objetivo asociada.
    """

    def __init__(self, size: int, function: IFunction):
        self.result: list[Variable] = []
        self.valueResult: np.ndarray = np.array(function.obtain_array_vector())
        self.size = size

    def addVariable(self, variable: Variable):
        """Agrega una variable si no se ha alcanzado el tamaño máximo."""
        if len(self.result) < self.size:
            self.result.append(variable)