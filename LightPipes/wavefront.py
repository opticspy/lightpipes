# -*- coding: utf-8 -*-


import numpy as _np
from .core import Phase, PhaseUnwrap, Intensity

def Wavefront_ptv(F, units='opd'):
    """
    Calculate the peak to valley (PtV) abberation of the wavefront of the
    given field. Only tested to work with a contiguous field in a centered
    aperture with a phase that can be unwrapped without problems.
    
    units: as used in Phase(). Default is 'opd'
    """
    pmap = Phase(F, unwrap=True, units=units, blank_eps=1e-3)
    ptv = _np.nanmax(pmap) - _np.nanmin(pmap) #[rad]
    return ptv

def Wavefront_rms(F, units='opd'):
    """
    Calculate the root-mean-square (rms) deviation of the wavefront of the
    given field. Only tested to work with a contiguous field in a centered
    aperture with a phase that can be unwrapped without problems.
    
    units: as used in Phase(). Default is 'opd'
    """
    pmap = Phase(F, unwrap=True, units=units, blank_eps=1e-3)
    mean = _np.nanmean(pmap)
    pmap -= mean #set data to mean 0
    target = _np.zeros_like(pmap) #target is a flat phase front
    targetflat = target[~_np.isnan(pmap)]
    pmapflat = pmap[~_np.isnan(pmap)]
    rms = _np.sqrt(((pmapflat - targetflat)** 2).mean())
    return rms