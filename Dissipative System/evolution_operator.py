from qiskit import QuantumCircuit

def evolution_operator(n0,tau,system_pulse,env_mode_pulses,couplings):
    nspins = len(env_mode_pulses)+1
    circuit = QuantumCircuit(nspins)
    for i in range(n0):
        circuit.rz(-system_pulse*tau/n0,0)
        for j in range(1,nspins):
            circuit.rz(-env_mode_pulses[j-1]*tau/n0,j)
            circuit.barrier()
            circuit.rxx(tau*couplings[j-1]/n0,0,j)
            circuit.barrier()
    return circuit
