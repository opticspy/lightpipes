# -*- coding: utf-8 -*-


import numpy as _np

from .units import *
from .core import Phase, PhaseUnwrap, Intensity

def Plot(F, unwrap = False, phaseblank =True, title='', circ_r=None, zoom=1,
         ph_units='rad', figsize = None):
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
    :param ph_units: Units to plot phase in (rad, opd, lam, default=rad)
    Returns
    -------
    (fig, (ax_left, ax_right)) handles in a tuple.

    """
    
    import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=figsize)
    ax1, ax2 = axs
    
    if title:
        fig.suptitle(title)
    PlotIntensity(F, circ_r, zoom, ax=ax1)
    PlotPhase(F, unwrap, phaseblank, circ_r, zoom, ph_units= ph_units, ax=ax2)
    return fig, axs


def PlotIntensity(F, circ_r=None, zoom=1, title='',
         ax=None, **kwargs):
    """
    Plot the field intensity with matplotlib. If ax is specified,
    add the plot to this ax instead of creating a new figure

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
    
    if ax is None:
        fig, ax = plt.subplots(1, 1, **kwargs)
        fig.suptitle(title)
        ax.set_title('Intensity')
    else:
        if title:
            ax.set_title(title)
        else:
            ax.set_title('Intensity')
    
    I = Intensity(0,F)
    
    ax.imshow(I, extent=extent)
    ax.set_xlabel(unit_txt)
    ax.set_xlim(xmin/zoom/units, xmax/zoom/units)
    ax.set_ylim(xmax/zoom/units, xmin/zoom/units) #y top is negative
    
    if circ_r is not None:
        circle = mpatches.Circle([0, 0], circ_r/units, fc='#ff000000',
                                 ec="grey", linestyle='--')
        ax.add_patch(circle)

def PlotPhase(F, unwrap = False, phaseblank =True, circ_r=None,
              zoom=1, title='', ax=None, ph_units='rad', **kwargs):
    """
    Plot the field intensity with matplotlib. If ax is specified,
    add the plot to this ax instead of creating a new figure

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
    
    if ax is None:
        fig, ax = plt.subplots(1, 1, **kwargs)
        fig.suptitle(title)
    
    blank_eps = 1/256 if phaseblank else 0
    #since 8bit screen cannot show difference then (in grayscale at least...)
    Phi = Phase(F, unwrap=unwrap, blank_eps=blank_eps, units=ph_units)
    
    if not unwrap:
        im  = ax.imshow(Phi, extent=extent, vmin=-_np.pi, vmax=_np.pi)
    else:
        im  = ax.imshow(Phi, extent=extent)
    ax.set_xlabel(unit_txt)
    ax.set_xlim(xmin/zoom/units, xmax/zoom/units)
    ax.set_ylim(xmax/zoom/units, xmin/zoom/units) #y min is top
    ax.set_title('Phase map'+(' (wrapped)' if not unwrap else ' (unwrapped)'))
    
    if circ_r is not None:
        circle = mpatches.Circle([0, 0], circ_r/units, fc='#ff000000',
                                 ec="grey", linestyle='--')
        ax.add_patch(circle)
    cbar = plt.colorbar(im, ax=ax)
    if ph_units=='rad':
        cbar.ax.set_ylabel('phase angle [rad]')
    elif ph_units=='lam':
        cbar.ax.set_ylabel('phase delay [lambda]')
    elif ph_units=='opd':
        cbar.ax.set_ylabel('phase delay [opd]')
    else:
        cbar.ax.set_ylabel('phase delay')
    if not unwrap:
        cbar.set_ticks([-_np.pi, -_np.pi/2, 0, _np.pi/2, _np.pi])
        cbar.ax.set_yticklabels(['-pi', '', '0', '', 'pi'])
    else:
        pass# would need more fancy way to find max etc to manually set
        # correct ticks...



def PlotCompareI(F1, F2, title='', title1='', title2='', circ_r=None, zoom=1):
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
        fig.suptitle(title)
    if title1:
        ax1.set_title(title1)
    if title2:
        ax2.set_title(title2)
    return fig

