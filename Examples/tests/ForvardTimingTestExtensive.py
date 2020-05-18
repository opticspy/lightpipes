"""
Timing test based on Young.py

Run the example setting for different grid sizes and record times.
Finally, create a plot of average time over N.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pickle
import os

from LightPipes import tictoc
from LightPipes.units import *

import LightPipes as lp

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

np.random.seed(123) #use same seed to get same pseudo-random numbers each run
N_pow, N_prime, N_comp = generate_N_list(8, 11, 6)

N_dict = {'pow':    N_pow,
          'prime':  N_prime,
          'comp':   N_comp}

runs_per_N = 3


#********* Run Forvard *******
print('Running test for Ns:')
print(N_dict)

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
            F=lp.Forvard(z,F)
            ttot = tictoc.toc()
            
            results_py_N[iN, jj] = ttot
    results_py[N_name] = results_py_N

pklfile = 'forvard_timing.pkl'
if os.path.exists(pklfile):
    print('Skipping save, file already exists.'
          + 'Delete or rename to save this run.')
else:
    pklobj = [N_dict, results_py]
    with open(pklfile,'xb') as f:
        pickle.dump(pklobj, f)
    

#*********** Plot results *******************
"""use pickle.load() to plot existing results."""
pklfile = 'forvard_timing.pkl'
with open(pklfile,'rb') as f:
    pklobj = pickle.load(f)
    N_dict = pklobj[0]
    results_py = pklobj[1]
pklfile_olp = 'forvard_timing_olp.pkl' #same run for old lightpipes
with open(pklfile_olp,'rb') as f:
    pklobj = pickle.load(f)
    N_dict_olp = pklobj[0]
    results_cpp = pklobj[1]
    
plt.plot(N_dict['pow'], np.average(results_py['pow'], axis=1),'o')
plt.plot(N_dict['prime'], np.average(results_py['prime'], axis=1),'*')
plt.plot(N_dict['comp'], np.average(results_py['comp'], axis=1),'+')
plt.plot(N_dict_olp['pow'], np.average(results_cpp['pow'], axis=1),'o')
plt.plot(N_dict_olp['prime'], np.average(results_cpp['prime'], axis=1),'*')
plt.plot(N_dict_olp['comp'], np.average(results_cpp['comp'], axis=1),'+')
plt.yscale('log')
plt.xscale('log')
plt.title('Comparison of reference LightPipes Cpp vs. new Python implementation')
plt.xlabel('N')
plt.ylabel('Time for 1 call to Forvard [s]')
plt.legend(['Py - power of 2', 'Py - prime', 'Py - composite',
            'Cpp - power of 2', 'Cpp - prime', 'Cpp - composite', ])

plt.show()
