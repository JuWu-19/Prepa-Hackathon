from helper import *
import pennylane as qml

def feature_map_ansatz(parameter,n_qubits,param_name= 'm0',n_layer=1,entanglement_type='full', interaction_type='z', interaction_length=2, full_rotation=False,symmetric=False, feature=True):
    '''ansatz composed of y rotation followed by a trainable feature map
    len(parameter)=[(1+2*full_rotation)*n_spins+len(int_list)]*n_layer
    '''

    int_list=possible_pair(entanglement_type,interaction_length,n_qubits)
    nbr_param = get_len_param(n_qubits,n_layer,interaction_length, entanglement_type,symmetric,full_rotation)
    count = 0
    name = entanglement_type+'_'+interaction_type+'_'+str(interaction_length)

    p_name = param_name[0]
    p_number = int((param_name[1:]))


    for i in range(n_layer):
        #y-rotation
        for j in range(n_qubits):
            if param_name[0]=='x':
                if j % 3 ==0:
                    qml.RX(parameter[count],wires = j)
                if j % 3 ==1:
                    qml.RY(parameter[count],wires = j)
                if j % 3 ==2:
                    qml.RZ(parameter[count],wires = j)

            else:
                qml.RY(parameter[count],wires = j)

            if not symmetric:
                count = count +1
            if full_rotation:
                qml.RX(parameter[count],wires = j)
                if not symmetric:
                    count = count +1
                qml.RY(parameter[count],wires = j)
                if not symmetric:
                    count = count +1
        if symmetric:
            count +=1


        #trainable feature map
        if feature:
            if interaction_type == 'x':
                qml.Hadamard(wires = np.range(n_qubits))
            if interaction_type =='y':
                qml.RX(np.pi/2,np.range(n_qubits))
            for interaction in int_list:

                for j in range(len(interaction)-1):
                    qml.CNOT(wires = [interaction[j],interaction[j+1]%n_qubits])
                qml.RZ(parameter[count],wires = interaction[-1]%n_qubits)
                if not symmetric:
                    count += 1
                for j in reversed(range(len(interaction)-1)):
                    qml.CNOT(wires = [interaction[j],interaction[j+1]%n_qubits])

            if interaction_type == 'x':
                qml.Hadamard(wires = np.range(n_qubits))
            if interaction_type =='y':
                qml.RX(np.pi/2,np.range(n_qubits))

            if symmetric:
                count +=1
