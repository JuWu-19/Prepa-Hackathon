import numpy as np
import scipy as sc
from qiskit.circuit                        import QuantumCircuit,ClassicalRegister, QuantumRegister
from qiskit.opflow.gradients               import Gradient
from qiskit.opflow.state_fns               import CircuitStateFn, StateFn
from qiskit.opflow.expectations            import PauliExpectation
from qiskit.opflow.converters              import CircuitSampler

from qiskit.opflow import I, Z, Zero, TensoredOp, PauliSumOp, PauliOp, \
                        PauliTrotterEvolution, Gradient, \
                        StateFn, CircuitStateFn, CircuitSampler

from qiskit.opflow.evolutions              import Suzuki, Trotter

from qiskit.opflow.expectations  import PauliExpectation, AerPauliExpectation, MatrixExpectation

# from qiskit.algorithms.optimizers.aqgd    import AQGD
from algorithm.AQGD import AQGD
from ansatz.ansatz import feature_map_ansatz


class VQE:
    def __init__(self,hamiltonian,n_qubits,instance, shots):

        self.hamiltonian        = hamiltonian
        self.instance           = instance
        self.n_qubits           = n_qubits
        self.shots              = shots
        self.P0                 = (I + Z) / 2
        self.P1                 = (I - Z) / 2
        self.optimal_parameters = {}
        self.cost               = {}
        self.shift_energy       = 100


    def ansatz(self, n_layer, entanglement_type = 'full', int_type = 'z', int_len=2, full_rotation = False,symmetric = False, feature_map = True):

        ansatz = lambda parameter: feature_map_ansatz(parameter,self.n_qubits,n_layer,entanglement_type=entanglement_type, interaction_type= int_type,
            interaction_length=int_len, full_rotation=full_rotation,symmetric=symmetric)

        return ansatz

    def excited_states(self,parameters,i):
        #Make the operator measurable
        op = StateFn(self.hamiltonian,is_measurement = True)

        # create the wavefunction
        wfn = CircuitStateFn(self.ansatz(parameter=parameters))

        braket = op @ wfn  #matrix product

        # Simulate the sampling
        grouped = PauliExpectation().convert(braket)
        sampled_op = CircuitSampler(self.instance).convert(grouped)

        # Expectation value
        mean_value = sampled_op.eval().real
        est_err = 0
        var_overlap = 0
        for j in range(i):
            overlap, var = self.overlap(parameters,j)
            var_overlap += var
            mean_value += self.shift_energy*overlap

        # If the simulations is not unitary evolution, return an error bar
        if (not self.instance.is_statevector):
            variance = PauliExpectation().compute_variance(sampled_op).real + var_overlap
            est_err  = np.sqrt(variance/shots)

        return mean_value, est_err


    def update(self,parameters,level=0):
        try:
            a = self.cost[str(level)]
            parameters = self.optimal_parameters[str(level)]
        except:
            self.cost[str(level)] = list([self.excited_states(parameters,level)[0]])

        parameters = np.array(parameters)
        AQGD_ = AQGD(maxiter= 50, eta = 0.1, tol= 1e-6,  momentum = 0.9, param_tol = 1e-6)

        new_parameters, cost, _ = AQGD_.optimize(num_vars=len(parameters),objective_function= lambda parameters: self.excited_states(parameters,level)[0],
        initial_point = parameters)

        self.cost[str(level)] += list(cost)

        if cost[-1] <= min(self.cost[str(level)]):
            self.optimal_parameters[str(level)] = new_parameters

        return new_parameters

    def SWAP_test(self,parameters,j):
        a = QuantumRegister(1,name='a')
        q1 = QuantumRegister(self.n_qubits,name='q1')
        q2 = QuantumRegister(self.n_qubits,name='q2')
        swap_test = QuantumCircuit(a,q1,q2)
        swap_test.h(a)
        swap_test = swap_test.compose(self.ansatz(parameters),qubits= q1)
        swap_test = swap_test.compose(self.ansatz(self.optimal_parameters[str(j)]),qubits= q2)
        for i in range(self.n_qubits):
            swap_test.cswap(a,q1[i],q2[i])
        swap_test.h(a)

        swap_test = CircuitStateFn(swap_test)

        proj0=StateFn(TensoredOp([self.P0] * (self.n_qubits)),is_measurement = True)
        braket = proj0 @ swap_test
        grouped = MatrixExpectation().convert(braket)
        sampled_op = CircuitSampler(self.instance).convert(grouped)
        overlap = sampled_op.eval().real
        var_overlap = 0

        if (not self.instance.is_statevector):
            variance = PauliExpectation().compute_variance(sampled_op).real
            var_overlap  = np.sqrt(variance/shots)

        return overlap, var_overlap

    def overlap(self,parameters, i):

        proj0=StateFn(TensoredOp([self.P0] * (self.n_qubits)),is_measurement = True)
        proj = self.projector(i)

        out_product = CircuitStateFn(self.ansatz(parameters).inverse().compose(self.ansatz(self.optimal_parameters[str(i)])))
        braket = proj0 @ out_product
        grouped = MatrixExpectation().convert(braket)
        sampled_op = CircuitSampler(self.instance).convert(grouped)
        overlap = sampled_op.eval().real

        var_overlap = 0
        if (not self.instance.is_statevector):
            variance = PauliExpectation().compute_variance(sampled_op).real
            var_overlap  = np.sqrt(variance/shots)

        return overlap, var_overlap

    def projector(self,i):
        bit =bin(i)[2:]
        if len(bit)<self.n_qubits:
            proj = TensoredOp([self.P0] * (self.n_qubits-len(bit)))
        else:
            proj = 1
        for j in bit:
            if j==str(0):
                proj =  proj ^ self.P0
            else:
                proj =  proj ^ self.P1

        return StateFn(proj,is_measurement = True)

    def compute_vqe_energy(self,level):
        energy, err = self.excited_states(self.optimal_parameters[str(level)],level)


    def compute_exact_energy(self):
        energies,_  = np.linalg.eigh(self.hamiltonian.to_matrix())
        return energies
