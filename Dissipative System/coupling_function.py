import numpy as np

def coupling_function(pulse,deltapulse,pulsec = 100,alpha=0.0002):
    return 2*np.sqrt(alpha*pulsec/np.pi)*np.exp(-pulse/2/pulsec)*np.sqrt(pulsec*np.cosh(deltapulse/2/pulsec)-deltapulse/2*np.sinh(deltapulse/2/pulsec))