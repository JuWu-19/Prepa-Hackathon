import numpy as np
from qiskit import QuantumCircuit
import qiskit.quantum_info as qi

def spin_bath_equilibrium(T,omegas):
    length = len(omegas)
    probabilities = np.zeros(length)
    rho = []
    for j in range(length):
        probabilities[j] = 1/(1+np.exp(omegas[j]/T))
        rho.append(np.array([[1-probabilities[j],0],[0,probabilities[j]]]))
    environment_density_matrix = qi.DensityMatrix(rho[0])
    for j in range(length-1):
        environment_density_matrix = environment_density_matrix.tensor(qi.DensityMatrix(rho[j+1]))
    return environment_density_matrix