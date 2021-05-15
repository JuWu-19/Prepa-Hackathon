import itertools
import numpy as np

def possible_pair(type,interaction,n_spins):

    # give all possible list of ascending integers between  i and j

    List=[]
    if type == 'linear':
        for j in range(1,interaction+1):
            for i in range(n_spins-1):
                if i+j>n_spins-1:
                    continue
                a=[i]
                for k in range(j):
                    a.append(i+k+1)
                List.append(a)

    elif type == 'circular':

        for j in range(1,interaction+1):
            for i in range(n_spins):
                if i+j>n_spins:
                    continue
                a=[i]
                for k in range(j):
                    a.append((i+k+1)%n_spins)
                List.append(a)

    elif type == 'full':
        for i in range(n_spins):
            for j in range(i+1,n_spins):
                for l in range(j-i):
                    a=[i]
                    b = itertools.combinations(range(i+1,j),l)
                    for it in b:
                        c = a+list(it)
                        c.append(j)
                        List.append(c)
    else:
        print('entanglement type not valid')
    c=0
    for a in range(len(List)):
        if len(List[a-c])>interaction+1 :
            del List[a-c]
            c+=1

    return List

def len_param(n_qubits,n_layer,interaction_length, entanglement_type ='full',feature_map=True,symmetric=False,full_rotation=False):
    l=0
    if feature_map:
        if symmetric:
            l = 2*n_layer
        else:
            l_int = len(possible_pair(entanglement_type,interaction_length,n_qubits))
            l = (1+2*int(full_rotation))*n_qubits+l_int
            l *= n_layer

    else:
        l=2**n_qubits

    return l
