# -*- coding: utf-8 -*-


import numpy as _np

from .units import *
from .core import Phase, PhaseUnwrap, Intensity

def Plot(F, unwrap = False, phaseblank =True, title='', circ_r=None, zoom=1):
    """
    Plot the field intensity and phase with matplotlib.

    Parameters
    ----------
    F : TYPE
        DESCRIPTION.
    unwrap : TYPE, optional
        DESCRIPTION. The default is False.
    phaseblank : TYPE, optional
        DESCRIPTION. The default is True.
    title : TYPE, optional
        DESCRIPTION. The default is ''.
    circ_c : float, optional
        [m] radius of a circle to draw. The default is None, i.e. circle off.

    Returns
    -------
    None.

    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    L = F.siz
    xmin = -L/2
    xmax = L/2
    dx = F.dx
    units = mm #[m] set if display should be in um/mm/...
    unit_txt = 'mm'
    if L < 3*mm:
        units = um
        unit_txt = 'um'
    
    extent = [(xmin-0.5*dx)/units, (xmax+0.5*dx)/units,
              (xmax+0.5*dx)/units, (xmin-0.5*dx)/units]#lrbt
    
    fig, axs = plt.subplots(1,2)
    ax1, ax2 = axs
    I = Intensity(0,F)
    Phi = Phase(F)
    if unwrap:
        Phi = PhaseUnwrap(Phi)
    Imax = I.max()
    Ithresh = Imax/256 #since screen cannot show difference then (in grayscale at least...)
    if phaseblank:
        Phi[I<Ithresh] = _np.nan
    ax1.imshow(I, extent=extent)
    ax1.set_xlabel(unit_txt)
    ax1.set_xlim(xmin/zoom/units, xmax/zoom/units)
    ax1.set_ylim(xmin/zoom/units, xmax/zoom/units)
    
    if circ_r is not None:
        circle = mpatches.Circle([0, 0], circ_r/units, fc='#ff000000',
                                 ec="grey", linestyle='--')
        ax1.add_patch(circle)
    im  = ax2.imshow(Phi, extent=extent)
    ax2.set_xlim(xmin/zoom/units, xmax/zoom/units)
    ax2.set_ylim(xmin/zoom/units, xmax/zoom/units)
    
    if circ_r is not None:
        circle = mpatches.Circle([0, 0], circ_r/units, fc='#ff000000',
                                 ec="grey", linestyle='--')
        ax2.add_patch(circle)
    fig.colorbar(im)
    if title:
        ax1.set_title(title)
    # return I, Phi #deprecated, now can easily be done with LPInt/LPPhase


def PlotCompareI(F1, F2, title='', circ_r=None, zoom=1):
    """
    Plot the field intensity for Field 1 and 2 with coupled scales

    Parameters
    ----------
    

    Returns
    -------
    None.

    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    L1 = F1.siz
    x1min = -L1/2
    x1max = L1/2
    d1x = F1.dx
    
    L2 = F2.siz
    x2min = -L2/2
    x2max = L2/2
    d2x = F2.dx
    
    L = L1
    xmin = x1min
    xmax = x1max
    dx = d1x #TODO make this more versatile, now assuming F1 and F2 same size
    
    units = mm #[m] set if display should be in um/mm/...
    unit_txt = 'mm'
    if L1 < 3*mm:
        units = um
        unit_txt = 'um'
    
    extent = [(xmin-0.5*dx)/units, (xmax+0.5*dx)/units,
              (xmax+0.5*dx)/units, (xmin-0.5*dx)/units]#lrbt
    
    
    I1 = Intensity(0,F1)
    I2 = Intensity(0,F2)
    
    fig, axs = plt.subplots(1,2)
    ax1, ax2 = axs
    ax1.imshow(I1, extent=extent)
    ax1.set_xlabel(unit_txt)
    ax1.set_xlim(xmin/zoom/units, xmax/zoom/units)
    ax1.set_ylim(xmin/zoom/units, xmax/zoom/units)
    
    if circ_r is not None:
        circle = mpatches.Circle([0, 0], circ_r/units, fc='#ff000000',
                                 ec="grey", linestyle='--')
        ax1.add_patch(circle)
    
    im  = ax2.imshow(I2, extent=extent)
    ax2.set_xlim(xmin/zoom/units, xmax/zoom/units)
    ax2.set_ylim(xmin/zoom/units, xmax/zoom/units)
    
    if circ_r is not None:
        circle = mpatches.Circle([0, 0], circ_r/units, fc='#ff000000',
                                 ec="grey", linestyle='--')
        ax2.add_patch(circle)
    # fig.colorbar(im)
    if title:
        ax1.set_title(title)
    # return I, Phi #deprecated, now can easily be done with LPInt/LPPhase


