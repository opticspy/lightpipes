# -*- coding: utf-8 -*-



import numpy as _np
from numpy import pi as _pi

def UNWRAP(ol, co, factor, hfactor):
    val = ol
    if val-co >= hfactor:
        while val-co >= hfactor:
            val -= factor
    elif val-co <= -hfactor:
        while val-co <= -hfactor:
            val += factor
    ne = val
    return ne


def unwrap_phase(Phi):
    """
    Attempt to unwrap the phase of the input. If data is noisy/unsmooth,
    this may result in unphysical patterns. In this case, try a finer sampling.

    Parameters
    ----------
    Phi : ndarray (MxN), real
        Real phase of size M (in y) and N (in x).

    Returns
    -------
    ndarray of same shape as input, with phase values unwrapped

    """
    #Checked functionality, gives similar results to Cpp code -> OK
    ysize, xsize = Phi.shape
    ibuffer = Phi.flatten()
    
    obuffer = _np.zeros_like(ibuffer)
    p = 0 #pointer/array index in flat array inbuffer, point to first el
    q = 0 #pointer to outbuffer
    hxsize = xsize >> 1 #x/2
    hysize = ysize >> 1
    hfactor = _pi
    factor = 2*_pi
    
    """
    /* position p in centre of image */
    /* central pixel */
    """
    p += hysize*xsize + hxsize
    q += hysize*xsize + hxsize
    obuffer[q] = ibuffer[p] #central pixel
    """
    /* first shell of pixels */
    /* north */
    """
    comval = obuffer[q]
    oldpix = ibuffer[p-xsize]
    obuffer[q-xsize] = UNWRAP(oldpix, comval, factor, hfactor)
    """ /* east */
    """
    comval = (obuffer[q-xsize]
            + obuffer[q])/2
    oldpix = ibuffer[p+1]
    obuffer[q+1] = UNWRAP(oldpix, comval, factor, hfactor)
    """ /* south */
    """
    comval = (obuffer[q+1]
            + obuffer[q])/2
    oldpix = ibuffer[p+xsize]
    obuffer[q+xsize] = UNWRAP(oldpix, comval, factor, hfactor)
    """ /* west */
    """
    comval = (obuffer[q+xsize]+obuffer[q])/2
    oldpix = ibuffer[p-1]
    obuffer[q-1] = UNWRAP(oldpix, comval, factor, hfactor)
    
    """ /* north-west */
    """
    comval = (obuffer[q-xsize]+obuffer[q-1]+obuffer[q])/3
    oldpix = ibuffer[p-xsize-1]
    obuffer[q-xsize-1] = UNWRAP(oldpix, comval, factor, hfactor)
    """ /* north-east */
    """
    comval = (obuffer[q-xsize]+obuffer[q+1]+obuffer[q])/3
    oldpix = ibuffer[p-xsize+1]
    obuffer[q-xsize+1] = UNWRAP(oldpix, comval, factor, hfactor)
    """ /* south-east */
    """
    comval = (obuffer[q+xsize]+obuffer[q+1]+obuffer[q])/3
    oldpix = ibuffer[p+xsize+1]
    obuffer[q+xsize+1] = UNWRAP(oldpix, comval, factor, hfactor)
    """ /* south-west */
    """
    comval = (obuffer[q+xsize]+obuffer[q-1]+obuffer[q])/3
    oldpix = ibuffer[p+xsize-1]
    obuffer[q+xsize-1] = UNWRAP(oldpix, comval, factor, hfactor)
    
    """
    /************ next shells ***********/
    """
    i = 1
    j = 0
    i += 1
    while i < hxsize:
        """/* north */
        """
        comval = (obuffer[q - (i-1)*xsize - i + 1]
                + obuffer[q - (i-1)*xsize - i + 2])/2
        oldpix = ibuffer[p - i*xsize - i + 1]
        obuffer[q - i*xsize - i + 1] = UNWRAP(oldpix, comval, factor, hfactor)
        
        j = i-1
        j -= 1
        while j > -i:
            comval = (obuffer[q - i*xsize - j - 1]
                    + obuffer[q - (i-1)*xsize - j]
                    + obuffer[q - (i-1)*xsize - j - 1])/3
            oldpix = ibuffer[p - i*xsize - j]
            obuffer[q - i*xsize - j] = UNWRAP(oldpix, comval, factor, hfactor)
            j -= 1
        
        """/* south */
        """
        comval = (obuffer[q + (i-1)*xsize + i - 1]
                + obuffer[q + (i-1)*xsize + i - 2])/2
        oldpix = ibuffer[p + i*xsize + i - 1]
        obuffer[q + i*xsize + i - 1] = UNWRAP(oldpix, comval, factor, hfactor)
        
        j = i-1
        j -= 1
        while j > -i:
            comval = (obuffer[q + i*xsize + j + 1]
                    + obuffer[q + (i-1)*xsize + j]
                    + obuffer[q + (i-1)*xsize + j + 1])/3
            oldpix = ibuffer[p + i*xsize + j]
            obuffer[q + i*xsize + j] = UNWRAP(oldpix, comval, factor, hfactor)
            j -= 1
        
        """/* east */
        """
        comval = (obuffer[q + i - 1 - (i-1)*xsize]
                + obuffer[q + i - 1 - (i-2)*xsize])/2
        oldpix = ibuffer[p + i - (i - 1)*xsize]
        obuffer[q + i - (i - 1)*xsize] = UNWRAP(
                oldpix, comval, factor, hfactor)
        
        j = i-1
        j -= 1
        while j > -i:
            comval = (obuffer[q + i - (j+1)*xsize]
                    + obuffer[q + i - 1 - (j+1)*xsize]
                    + obuffer[q + i - 1 - j*xsize])/3
            oldpix = ibuffer[p + i - j*xsize]
            obuffer[q + i - j*xsize] = UNWRAP(oldpix, comval, factor, hfactor)
            j -= 1
        
        """/* west */
        """
        comval = (obuffer[q - i + 1 + (i-1)*xsize]
                + obuffer[q - i + 1 + (i-2)*xsize])/2
        oldpix = ibuffer[p - i + (i - 1)*xsize]
        obuffer[q - i + (i - 1)*xsize] = UNWRAP(
                oldpix, comval, factor, hfactor)
        
        j = i-1
        j -= 1
        while j > -i:
            comval = (obuffer[q - i + (j+1)*xsize]
                    + obuffer[q - i + 1 + (j+1)*xsize]
                    + obuffer[q - i + 1 + j*xsize])/3
            oldpix = ibuffer[p - i + j*xsize]
            obuffer[q - i + j*xsize] = UNWRAP(oldpix, comval, factor, hfactor)
            j -= 1
        
        """/* north-west */
        """
        comval = (obuffer[q - (i-1)*xsize - i]
                + obuffer[q - i*xsize - i + 1]
                + obuffer[q - (i-1)*xsize - i + 1])/3
        oldpix = ibuffer[p - i*xsize - i]
        obuffer[q - i*xsize - i] = UNWRAP(oldpix, comval, factor, hfactor)
        """ /* north-east */
        """
        comval = (obuffer[q - (i-1)*xsize + i]
                + obuffer[q - i*xsize + i - 1]
                + obuffer[q - (i-1)*xsize + i - 1])/3
        oldpix = ibuffer[p - i*xsize + i]
        obuffer[q - i*xsize + i] = UNWRAP(oldpix, comval, factor, hfactor)
        """ /* south-east */
        """
        comval = (obuffer[q + (i-1)*xsize + i]
                + obuffer[q + i*xsize + i - 1]
                + obuffer[q + (i-1)*xsize + i - 1])/3
        oldpix = ibuffer[p + i*xsize + i]
        obuffer[q + i*xsize + i] = UNWRAP(oldpix, comval, factor, hfactor)
        """ /* south-west */
        """
        comval = (obuffer[q + (i-1)*xsize - i]
                + obuffer[q + i*xsize - i + 1]
                + obuffer[q + (i-1)*xsize - i + 1])/3
        oldpix = ibuffer[p + i*xsize - i]
        obuffer[q + i*xsize - i] = UNWRAP(oldpix, comval, factor, hfactor)
        
        i += 1 #end of while
        
    """/* upper line and left column */
    """
    """
	/* upper line*/
    """
    comval = (obuffer[q - (hxsize-1)*xsize - hxsize + 1]
            + obuffer[q - (hxsize-1)*xsize - hxsize + 2])/2
    oldpix = ibuffer[p - hxsize*xsize - hxsize + 1]
    obuffer[q - hxsize*xsize - hxsize + 1] = UNWRAP(
            oldpix, comval, factor, hfactor)
    
    j = hxsize-1
    j -= 1
    while j > -hxsize:
        comval = (obuffer[q - hxsize*xsize - j - 1]
                + obuffer[q - (hxsize-1)*xsize - j]
                + obuffer[q - (hxsize-1)*xsize - j - 1])/3
        oldpix = ibuffer[p - hxsize*xsize - j]
        obuffer[q - hxsize*xsize - j] = UNWRAP(oldpix, comval, factor, hfactor)
        j -= 1
    """
	/* left line */
    """
    comval = (obuffer[q - hxsize + 1 + (hxsize-1)*xsize]
            + obuffer[q - hxsize + 1 + (hxsize-2)*xsize])/2
    oldpix = ibuffer[p - hxsize + (hxsize - 1)*xsize]
    obuffer[q - hxsize + (hxsize - 1)*xsize] = UNWRAP(
            oldpix, comval, factor, hfactor)
    
    j = hxsize-1
    j -= 1
    while j > -hxsize:
        comval = (obuffer[q - hxsize + (j+1)*xsize]
                + obuffer[q - hxsize + 1 + (j+1)*xsize]
                + obuffer[q - hxsize + 1 + j*xsize])/3
        oldpix = ibuffer[p - hxsize + j*xsize]
        obuffer[q - hxsize + j*xsize] = UNWRAP(oldpix, comval, factor, hfactor)
        j -= 1
    
    """ /* upper left corner */
    """
    comval = (obuffer[q - (hxsize-1)*xsize - hxsize]
            + obuffer[q - hxsize*xsize - hxsize + 1]
            + obuffer[q - (hxsize-1)*xsize - hxsize + 1])/3
    oldpix = ibuffer[p - hxsize*xsize - hxsize]
    obuffer[q - hxsize*xsize - hxsize] = UNWRAP(
            oldpix, comval, factor, hfactor)
    
    return obuffer.reshape((ysize,xsize))



