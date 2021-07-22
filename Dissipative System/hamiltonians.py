from qiskit.quantum_info import Pauli
from qiskit.opflow		  import PauliOp, SummedOp
import numpy as np

def open_system_hamiltonian(totspin):
    zspin = [0]*totspin
    xspin = [0]*totspin
    zspin[0] = 1
    zspin = np.asarray(zspin, dtype=bool)
    xspin = np.asarray(xspin, dtype=bool)
    return PauliOp(Pauli((zspin,xspin)),-0.5)

def environment_hamiltonian(frequencies):
    totspin = len(frequencies)+1
    paulis = []
    for j in range(1,totspin):
        zspin = [0] * totspin
        xspin = [0] * totspin
        zspin[j] = 1
        zspin = np.asarray(zspin, dtype=bool)
        xspin = np.asarray(xspin, dtype=bool)
        paulis.append(Pauli((zspin,xspin)))
    str = ''
    for i in range(len(frequencies)+1):
        str = str + 'I'
    env_h = PauliOp(Pauli(str),0)
    for j in range(totspin-1):
        env_h = env_h + PauliOp(paulis[j],frequencies[j])
    return env_h

def interaction_hamiltonian(couplings):
    for k in range(len(couplings)):
        couplings[k] = 0.5*couplings[k]
    env_spins = len(couplings)
    paulis = []
    for j in range(env_spins):
        zspin = [0] * env_spins
        xspin = [0] * env_spins
        xspin[j] = 1
        zspin = np.asarray(zspin, dtype=bool)
        xspin = np.asarray(xspin, dtype=bool)
        paulis.append(Pauli((zspin,xspin)))
    sum = PauliOp(paulis[0],couplings[0])
    for j in range(1,env_spins):
        sum = sum + PauliOp(paulis[j],couplings[j])
    inter_h = PauliOp(Pauli('X'))
    return inter_h.tensor(sum)

