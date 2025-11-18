from abc import ABC, abstractmethod
import math
import numpy as np

class IFunction(ABC):
    @property
    @abstractmethod
    def vector_size(self)->int:
        pass
    
    @vector_size.setter
    @abstractmethod
    def vector_size(self, val):
        pass
    
    @property
    @abstractmethod
    def variables(self)->list[float]:
        pass

    @variables.setter
    @abstractmethod
    def variables(self, val):
        pass
    
    @abstractmethod
    def execute(self)->float:
        pass

    @abstractmethod
    def obtain_array_vector(self)->list[float]:
        pass

    @abstractmethod
    def initialize_vector(self):
        pass
        
class Variable:
    
    def __init__(self, value:float):
        self.value:float = value

class QuadraticFunction(IFunction):
    
    def __init__(self, a:float, b:float, c:float, d:float):
        self.a:float = a
        self.b:float = b
        self.c:float = c
        self.d:float = d
        self.variables= []
        self.vector_size = 2
        self.initialize_vector()
        
        
    @property
    def vector_size(self)->int:
        return self._vector_size

    @vector_size.setter
    def vector_size(self, val):
        self._vector_size = val
        
    @property
    def variables(self)->list[float]:
        return self._variables

    @variables.setter
    def variables(self, val):
        self._variables = val
        
    def initialize_vector(self):
        for i in range(self.vector_size):
            self.variables.append(0)
    
    def execute(self):
        x = self.variables[0]
        y = self.variables[1]
        return self.a*math.pow((x-self.b),2)+self.c*math.pow((y-self.d),2)
    
    def add_variable(self, variable: float):
        self.variables.append(variable)
        
    def obtain_array_vector(self) -> list[float]:
        vector:list[float] = []
        for i in range(len(self.variables)):
            vector.append(0)
        return vector
        
class RosenbrockFunction(IFunction):
    
    def __init__(self, a:float, b:float):
        self.a:float = a
        self.b:float = b
        self.variables= []
        self.vector_size = 2
        self.initialize_vector()
        
    @property
    def vector_size(self)->int:
        return self._vector_size

    @vector_size.setter
    def vector_size(self, val):
        self._vector_size = val
        
    @property
    def variables(self)->list[float]:
        return self._variables

    @variables.setter
    def variables(self, val):
        self._variables = val
        
    def initialize_vector(self):
        for i in range(self.vector_size):
            self.variables.append(0)
    
    def execute(self):
        x = self.variables[0]
        y = self.variables[1]
        return self.a*math.pow((self.b-x),2)+math.pow((y-math.pow(x,2)),2)
    
    def add_variable(self, variable: float):
        self.variables.append(variable)
        
    def obtain_array_vector(self) -> list[float]:
        vector:list[float] = []
        for i in range(len(self.variables)):
            vector.append(0)
        return vector
        
class RastriginFunction(IFunction):
    
    def __init__(self, A:float, n:int):
        self.A:float = A
        self.n:int = n
        self.variables= []
        self.vector_size = n
        self.initialize_vector()
        
    @property
    def vector_size(self)->int:
        return self._vector_size

    @vector_size.setter
    def vector_size(self, val):
        self._vector_size = val
        
    @property
    def variables(self)->list[float]:
        return self._variables

    @variables.setter
    def variables(self, val):
        self._variables = val
        
    def initialize_vector(self):
        for i in range(self.vector_size):
            self.variables.append(0)
    
    def execute(self):
        sumatory = 0
        for i in range(self.n):
            x_i = self.variables[i]
            sumatory+=(math.pow(x_i,2)-self.A*math.cos(2*math.pi*x_i))
        return self.A*self.n+sumatory
    
    def add_variable(self, variable: float):
        self.variables.append(variable)
        
    def obtain_array_vector(self) -> list[float]:
        vector:list[float] = []
        for i in range(len(self.variables)):
            vector.append(0)
        return vector
        
class BoundedVariable(Variable):
    
    def __init__(self, value:float, min_value:float, max_value:float):
        super().__init__(value)
        self.min_value:float = min_value
        self.max_value:float = max_value
        
    def isValidValue(self, value:float):
        return value >= self.min_value and value <= self.max_value

class VectorResult:
    
    def __init__(self, size:int, function:IFunction):
        self.result:list[Variable] = []
        self.valueResult:np.ndarray = np.array(function.obtain_array_vector())
        self.size = size
        
    def addVariable(self, variable:Variable):
        if self.size > len(self.result):
            self.result.append(variable)