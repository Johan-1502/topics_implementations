import numpy as np
print(np.abs(-3))
#
#vector = np.array([2,5])
#operation = vector*0.9
#print(operation)

from function import QuadraticFunction, RosenbrockFunction, RastriginFunction
from pso import PSO

#function = QuadraticFunction(1,2,3,4)
#simulator = PSO()
#simulator.calculate_function(30, 80, function, True)

function = RosenbrockFunction(1,2)
simulator = PSO()
simulator.calculate_function(30, 80, function, True)

#function = RastriginFunction(10, 2)
#simulator = PSO()
#simulator.calculate_function(30, 80, function, True)


