from qiskit.aqua.algorithms import VQE, NumPyEigensolver
import matplotlib.pyplot as plt
import numpy as np
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.components.initial_states import HartreeFock
from qiskit.circuit.library import EfficientSU2
from qiskit.aqua.components.optimizers import COBYLA, SPSA, SLSQP
from qiskit.aqua.operators import Z2Symmetries
from qiskit import IBMQ, BasicAer, Aer
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.chemistry import FermionicOperator
from qiskit.aqua import QuantumInstance
from qiskit.ignis.mitigation.measurement import CompleteMeasFitter
from qiskit.providers.aer.noise import NoiseModel
from qiskit.quantum_info.operators import Operator
from qiskit.aqua.operators.primitive_ops import PrimitiveOp
from qiskit.opflow.primitive_ops import PauliSumOp

from Hamiltonian import *
from ansatz import *

'''
Run Qiskit VQE
'''

backend = BasicAer.get_backend("statevector_simulator")
optimizer = SLSQP(maxiter = 5)
#   Define the Hamiltonian
n_spins = 3
J_x = 1
J_y = 1
J_z = 1
h = 1
hamiltonian = generate_XYZ(J_x, J_y, J_z, h, n_spins)
#   Define the ansatz
parameter = np.zeros(10000)
n_layer = 3
ansatz = feature_map_ansatz(parameter,n_spins,n_layer)
#primitive = hamiltonian.primitive_strings()
#hamiltonian = PrimitiveOp(primitive)
print("Hamiltonian type: ",type(hamiltonian))
print("Ansatz type: ",type(ansatz))
vqe = VQE(hamiltonian,feature_map_ansatz,optimizer)
vqe_result = np.real(vqe.run(backend)['eigenvalue'])
