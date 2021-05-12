import numpy as np
import matplotlib.pyplot as plt
import qiskit
import qiskit.circuit
from qiskit.circuit import QuantumCircuit
from qiskit.aqua.operators import Z,I,X
from qiskit.aqua.operators.state_fns import CircuitStateFn
from qiskit.aqua.operators.expectations import PauliExpectation
from qiskit.aqua.operators import CircuitSampler, StateFn
from qiskit.quantum_info.operators.operator import Operator

fro Ham

H = (0.011280*Z^Z)+(0.397936*Z^I)+(0.397936*I^Z)+(0.180931*X^X)

def RY_ansatz(n_qubits,params):
    qc = QuantumCircuit(n_qubits)
    p_count = 0
    for i in range(n_qubits):
        qc.ry(params[p_count],i)
        p_count = p_count + 1
    qc.barrier()
    for i in range(n_qubits-1):
        qc.cx(i,i+1)
    qc.barrier()
    for i in range(n_qubits):
        qc.ry(params[p_count], i)
        p_count = p_count + 1
    return qc

def energy(n_qubits,op,ansatz,params,shots,instance):
    op = StateFn(op,is_measurement = True)
    wfn = CircuitStateFn(ansatz(n_qubits,params))
    braket = op @ wfn
    grouped = PauliExpectation().convert(braket)
    sampled_op = CircuitSampler(instance).convert(grouped)
    mean_value = sampled_op.eval().real
    est_err = 0
    if (not instance.is_statevector):
        variance = PauliExpectation().compute_variance(sampled_op).real
        est_err = np.sqrt(variance/shots)
    return mean_value, est_err

def ei(i,n):
	vi = np.zeros(n)
	vi[i] = 1.0
	return vi[:]

def gradient(n_qubits,op,ansatsz,params,shots,instance):
    n_params = len(params)
    wfn_circuits = []
    op = StateFn(op,is_measurement = True)
    for i in range(n_params):
        wfn_circuits.append(CircuitStateFn(RY_ansatz(n_qubits,params+ei(i,n_params)*np.pi/2.0)))
        wfn_circuits.append(CircuitStateFn(RY_ansatz(n_qubits, params - ei(i, n_params) * np.pi / 2.0)))
    results = []
    for wfn in wfn_circuits:
        braket = op @ wfn
        grouped = PauliExpectation().convert(braket)
        sampled_op = CircuitSampler(instance).convert(grouped)
        mean_value = sampled_op.eval().real
        est_err = 0
        if (not instance.is_statevector):
            variance = PauliExpectation().compute_variance(sampled_op).real
            est_err = np.sqrt(variance / shots)
        results.append([mean_value, est_err])
    g = np.zeros((n_params,2))
    for i in range(n_params):
        rplus = results[2*i]
        rminus = results[2*i+1]
        g[i, :] = (rplus[0] - rminus[0]) / 2.0, np.sqrt(rplus[1] ** 2 + rminus[1] ** 2) / 2.0
    return g

def VQE(n_qubits,op,ansatz,params,shots,instance,lr,n_reps):
    log={}
    log['energies'] = []
    log['err_energies'] = []
    log['gradients'] = []
    curr_params = params
    for i in range(n_reps):
        E = energy(n_qubits,op,ansatz,curr_params,shots,instance)
        print('Run number: ', i + 1)
        print('Energy:', E[0])
        print('========================= \n')
        log['energies'].append(E[0])
        log['err_energies'].append(E[1])
        g = gradient(n_qubits,op,ansatz,curr_params,shots,instance)
        print(g)
        curr_params = curr_params - lr*g[:,0]
    return log, curr_params

from qiskit.aqua import QuantumInstance
from qiskit import IBMQ, Aer
n_qubits = 2
params = np.zeros(4)
shots = 1
n_reps = 12
lr = 2
backend = Aer.get_backend('statevector_simulator')
instance = QuantumInstance(backend=backend,shots=shots)
res, params = VQE(n_qubits,H,RY_ansatz,params,shots,instance,lr,n_reps)

steps = list(range(n_reps))
plt.plot(steps,res['energies'],marker='o',linestyle='dashed')
plt.hlines(-1.175, xmin= 0.0, xmax=  11,label='Theoretical energy',linestyle ='dashed',color='grey')
plt.xlabel('Step')
plt.ylabel('Energy')
plt.grid(True)
#plt.show()

###
print("Hamiltonian type:", type(H))

### Try to compute the excited states with the same method

wfn = RY_ansatz(n_qubits, params)
print(Operator(RY_ansatz(n_qubits,params)))
