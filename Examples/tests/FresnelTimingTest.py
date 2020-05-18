"""
Timing test based on Young.py

Run the example setting for different grid sizes and record times.
Finally, create a plot of average time over N.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from LightPipes import tictoc
from LightPipes.units import *

import LightPipes as lp
"""reference LightPipes (Cpp) renamed and installed with "setup.py develop" as
oldLightPipes"""
import oldLightPipes as olp

print(lp.LPversion)
print(olp.LPversion)

def is_prime(n):
    """ from
    https://stackoverflow.com/questions/15285534/isprime-function-for-python-language
    
    """
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        # print '\t',f
        if n%f == 0: return False
        if n%(f+2) == 0: return False
        f +=6
    return True

def generate_N_list(m_min, m_max, count_between):
    """
    Generate three lists of different N:
        - a list of powers Nmin=2^m_min ... Nmax=2^m_max
        - a list of primes compiled for each interval between a power of 2
            and randomly truncated to length "count_between"
            counting in each interval, so the list may have up to
            (mmax-mmin)*count_between numbers
        - a list of composites in each interval as with primes
    """
    # following
    # https://blogs.mathworks.com/steve/2014/04/07/timing-the-fft/
    mlist = np.arange(m_min, m_max+1)
    N_pow = 2**mlist
    N_prime = []
    N_comp = []
    for mm in mlist[:-1]: #do not scan interval 2^mmax .. 2^(mmax+1)
        kk = np.arange(2**mm + 1, 2**(mm+1))
            #start +1 to exclude pow, stop excluded by default
        isp = np.zeros_like(kk,dtype=bool)
        for i, k in enumerate(kk):
            if is_prime(k):
                isp[i] = True
        primes = kk[isp]
        composites = kk[~isp]
        if len(primes) > count_between:
            #pick random subset
            primes = primes[
                np.random.permutation(len(primes))[:count_between]]
            primes.sort() #sort not necessary but for convenience
        if len(composites) > count_between:
            composites = composites[
                np.random.permutation(len(composites))[:count_between]]
            composites.sort() #sort not necessary but for convenience
        N_prime.append(primes)
        N_comp.append(composites)
    N_prime = np.asarray(N_prime).flatten()
    N_comp = np.asarray(N_comp).flatten()
    return N_pow, N_prime, N_comp


#******** Simulation parameters *************
wavelength=5*um
size=20.0*mm
z=50*cm
R=0.3*mm
d=1.2*mm

np.random.seed(123)
N_pow, N_prime, N_comp = generate_N_list(8, 12, 4)

# N_list=np.array([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
#         125, 126, 127, 128, 129, 130, 131, 132, 133,
#         150, 200, 250,
#         253, 254, 255, 256, 257, 258, 259, 260,
#         300, 350, 400, 450, 500,
#         501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514,
#         515, 516, 517, 518, 519, 520,
#         550, 600, 650, 700, 800, 900, 1000,
#         # 1010, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029,
#         # 1030,
#         # 1100, 1200, 1300, 1400,
#         # 1490, 1491, 1492, 1493, 1494, 1495, 1496, 1497, 1498, 1499, 1500,
#         # 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510,
#         # 1600, 1700, 1800, 1900,
#         # 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
#         # 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050,
#         # 2200, 2400, 2600, 2800, 3000,
#         ])

runs_per_N = 3


#********* Run for new python Fresnel *******

N_dict = {'pow':    N_pow,
          'prime':  N_prime,
          'comp':   N_comp}

results_py = {}
for N_name, N_list in N_dict.items():
    results_py_N = np.zeros((N_list.size, runs_per_N))
    
    for iN, N in enumerate(N_list):
        print(N) #progress update
        for jj in range(runs_per_N):
            F=lp.Begin(size,wavelength,N)
            F1=lp.CircAperture(R/2.0,-d/2.0, 0, F)
            F2=lp.CircAperture(R/2.0, d/2.0, 0, F)    
            F=lp.BeamMix(F1,F2)
            
            tictoc.tic()
            F=lp.Fresnel(z,F)
            ttot = tictoc.toc()
            results_py_N[iN, jj] = ttot
    results_py[N_name] = results_py_N

# tab = np.column_stack((N_list, results_py))
# np.savetxt('times_py3.txt', tab)

#****** Run for reference cpp Fresnel *******

# results_cpp = np.zeros((N_list.size, runs_per_N))

# for iN, N in enumerate(N_list):
#     print(N)
#     for jj in range(runs_per_N):
#         F=olp.Begin(size,wavelength,N)
#         F1=olp.CircAperture(R/2.0,-d/2.0, 0, F)
#         F2=olp.CircAperture(R/2.0, d/2.0, 0, F)    
#         F=olp.BeamMix(F1,F2)
        
#         tictoc.tic()
#         F=olp.Fresnel(z,F)
#         ttot = tictoc.toc()
#         results_cpp[iN, jj] = ttot

# tab = np.column_stack((N_list, results_cpp))
# np.savetxt('times_cpp3.txt', tab)

#*********** Plot results *******************
"""use np.loadtxt() to plot existing results."""
# results_py = np.loadtxt('times_py.txt')
# results_cpp = np.loadtxt('times_cpp.txt')
# N_list = results_py[:,0]
# results_py = results_py[:,1:] #strip N_list
# results_cpp = results_cpp[:,1:]

plt.scatter(N_dict['pow'], np.average(results_py['pow'], axis=1),
                                      marker='o',
                                      s=50)
plt.scatter(N_dict['prime'], np.average(results_py['prime'], axis=1),
                                      marker='*',
                                      s=50)
plt.scatter(N_dict['comp'], np.average(results_py['comp'], axis=1),
                                      marker='+',
                                      s=50)
plt.yscale('log')
plt.xscale('log')
# plt.scatter(N_list, np.average(results_cpp, axis=1))
# plt.title('Comparison of reference LightPipes Cpp vs. new Python implementation')
plt.xlabel('N')
plt.ylabel('Time for 1 call to Fresnel [s]')
plt.legend(['power of 2', 'prime', 'composite'])
