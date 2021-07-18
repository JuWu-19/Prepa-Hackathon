# Performances summary

##	17th of July

For the ground state, exact diagonalisation yields ground state at -3.46410162e+00. After 50 iterations of vqe, learning rate of 0.05, and the ansatz from p-VQD, the result is -2.969297942034383. Same amount of iterations but learning rate 0.1 yields: -3.300438299713924. Taking the number of iterations to 100 yields: -3.2338261976320135.
 
 Relancé la même simulation pour commencer le calcul du premier excité (probablement aux limites de l'ansatz): -3.3256001045720573.
 
 First time aiming at the 2 first energy levels: -3.3344755061644156 for the ground state and 9.15869915 for the first excited (targeting -2.00000000e+00). The a coefficient was 1000 (probably way too much). n_reps was 100. Trying with n_reps = 30 and a = 15: got -3.0625617660387414 and -1.39234935. Probably on the good way! Repeat with nreps = 100: -3.4076912934204397 and -1.997845294743496. Excellent.
 
 First try for the 8 energy levels:
 Exact diagonalisation				VQE
 -3.46410162e+00					-3.32934505595077
 -2.00000000e+00					-2.000077550505039
 -2.00000000e+00					-1.2728112331094232
 -4.72197789e-16					-0.1761220268221639
 -1.31221193e-16					-0.21088892502430207
 1.59329772e-16					1.0015900250949479
 3.46410162e+00					3.231412789551526
 4.00000000e+00					

Idea: increase a along the way, because when reaching the 6th level, a is absorbed into 5 levels, thus pretty much equivalent to a=3 for the first level. For example a\mapsto n*a.

-3.3158327969560197
-2.00011084448688
-0.7410893284107611
-0.3372807516421414
2.2404590719039716

Did not work.

##	18th of July

lr = 0.05, nsteps = 140. Got -3.2347661545087054 for the ground state. Retry with lr = 0.1. Got -3.320575073825103 which is better but probably not good enough. Going over 100 steps is not really useful. The ansatz does not seem to allow us to go closer to the ground state.
