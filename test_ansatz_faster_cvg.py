from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import itertools
import numpy as np

from ansatz import *

def test_ansatz(parameter,n_spins,n_layer,entanglement_type='full', interaction_length=2,full_rotation='False',test_number=2):
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
            for interaction in int_list:
                for j in range(len(interaction)-1):
                    circuit.cy(interaction[j], interaction[j + 1] % n_spins)
                    circuit.rz(parameter[count], interaction[-1] % n_spins)
                count += 1
    if test_number == 2:
        for j in range(n_layer):
            if (j%2==0):
                for i in range(n_spins):
                    circuit.rx(parameter[count],i)
                    count = count + 1
                circuit.barrier()
            if (j%2==1):
                for i in range(n_spins):
                    circuit.ry(parameter[count],i)
                    count = count + 1
                circuit.barrier()
                for i in range(n_spins-1):
                    circuit.rzz(parameter[count],i,i+1)
                    count = count+1
                circuit.barrier()

        if (n_layer%2==1):
            for i in range(n_spins):
                circuit.ry(parameter[count],i)
                count = count+1
        if (n_layer%2==0):
            for i in range(n_spins):
                circuit.rx(parameter[count],i)
                ++count


    return circuit
