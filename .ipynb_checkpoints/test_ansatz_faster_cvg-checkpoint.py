from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import itertools
import numpy as np

from ansatz import *

def test_ansatz(parameter,n_spins,n_layer,entanglement_type='full', interaction_length=2,full_rotation='False',test_number=1):
    int_list = possible_pair(entanglement_type,interaction_length,n_spins)
    count = 0
    circuit = QuantumCircuit(n_spins)
    if test_number == 1:
        for i in range(n_layer):
            for j in range(n_spins):
                circuit.ry(parameter[count],j)
                count = count + 1
                if full_rotation:
                    circuit.rx(parameter[count], j)
                    count = count + 1
                    circuit.ry(parameter[count], j)
                    count = count + 1
    return circuit
