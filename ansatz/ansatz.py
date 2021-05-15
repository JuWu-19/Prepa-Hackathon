import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from ansatz.helper import *

def feature_map_ansatz(parameter,n_qubits,n_layer,entanglement_type='full', interaction_type='z', interaction_length=2, full_rotation=False,symmetric=False):
    '''ansatz composed of y rotation followed by a trainable feature map
    len(parameter)=[(1+2*full_rotation)*n_spins+len(int_list)]*n_layer
    '''

    int_list=possible_pair(entanglement_type,interaction_length,n_qubits)
    count = 0
    name = entanglement_type+'_'+interaction_type+'_'+str(interaction_length)
    q = QuantumRegister(n_qubits)
    circuit = QuantumCircuit(q,name=name)

    for i in range(n_layer):
        #y-rotation
        for j in range(n_qubits):
            circuit.ry(parameter[count],j)

            if not symmetric:
                count = count +1
            if full_rotation:
                circuit.rx(parameter[count],j)
                if not symmetric:
                    count = count +1
                circuit.ry(parameter[count],j)
                if not symmetric:
                    count = count +1
        if symmetric:
            count +=1


        #trainable feature map
        if interaction_type == 'x':
            circuit.h(q)
        if interaction_type =='y':
            circuit.rx(np.pi/2,q)
        for interaction in int_list:

            for j in range(len(interaction)-1):
                circuit.cx(interaction[j],interaction[j+1]%n_qubits)
                circuit.rz(parameter[count],interaction[-1]%n_qubits)
                if not symmetric:
                    count += 1
            for j in reversed(range(len(interaction)-1)):
                circuit.cx(interaction[j],interaction[j+1]%n_qubits)

        if interaction_type=='x':
            circuit.h(q)
        if interaction_type =='y':
            circuit.rx(np.pi/2,q)
        if symmetric:
            count +=1
    return circuit
