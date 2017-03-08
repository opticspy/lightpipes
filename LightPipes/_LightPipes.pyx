# distutils: language = c++

import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
import webbrowser
import math

cdef extern from "lpspy.h" namespace "std":
    cdef cppclass lpspy:
        LightPipes() except +
        vector[vector[complex]] Axicon(double, double, double, double, vector[vector[complex]])
        vector[vector[complex]] BeamMix(vector[vector[complex]], vector[vector[complex]])      
        vector[vector[complex]] Begin(double, double, int)
        vector[vector[complex]] CircAperture(double, double, double, vector[vector[complex]])
        vector[vector[complex]] CircScreen(double, double, double, vector[vector[complex]])
        vector[vector[complex]] Convert(vector[vector[complex]])
        vector[vector[complex]] Forvard(double, vector[vector[complex]])       
        vector[vector[complex]] Fresnel(double, vector[vector[complex]])
        vector[vector[complex]] Gain(double, double, double, vector[vector[complex]])
        vector[vector[complex]] GaussAperture(double, double, double, double, vector[vector[complex]])      
        vector[vector[complex]] GaussScreen(double, double, double, double, vector[vector[complex]])
        vector[vector[complex]] GaussHermite(int, int, double, double, vector[vector[complex]])
        vector[vector[complex]] GaussLaguerre(int, int, double, double, vector[vector[complex]])
        vector[vector[complex]] IntAttenuator(double, vector[vector[complex]])               
        vector[vector[complex]] Lens(double, double, double, vector[vector[complex]])
        vector[vector[complex]] LensForvard(double, double, vector[vector[complex]])
        vector[vector[complex]] LensFresnel(double, double, vector[vector[complex]])
        vector[vector[complex]] MultIntensity(vector[vector[double]], vector[vector[complex]])
        vector[vector[complex]] MultPhase(vector[vector[double]], vector[vector[complex]])
        vector[vector[complex]] Normal(vector[vector[complex]])                   
        vector[vector[double]]  Intensity(int, vector[vector[complex]])
        vector[vector[complex]] Interpol(double, int, double, double, double, double, vector[vector[complex]])
        vector[vector[double]]  Phase(vector[vector[complex]])
        vector[vector[double]]  PhaseUnwrap(vector[vector[double]])        
        vector[vector[complex]] PipFFT(int, vector[vector[complex]])       
        double   				Power(vector[vector[complex]]);
        vector[vector[complex]] RandomIntensity(double, double, vector[vector[complex]]) 
        vector[vector[complex]] RandomPhase(double, double, vector[vector[complex]])                          
        vector[vector[complex]] RectAperture(double, double, double, double, double, vector[vector[complex]]) 
        vector[vector[complex]] RectScreen(double, double, double, double, double, vector[vector[complex]])
        vector[vector[complex]] Steps(double, int, vector[vector[complex]], vector[vector[complex]])
        double                  Strehl(vector[vector[complex]])
        vector[vector[complex]] SubIntensity(vector[vector[double]], vector[vector[complex]])
        vector[vector[complex]] SubPhase(vector[vector[double]], vector[vector[complex]])
        vector[vector[complex]] Tilt(double ,double, vector[vector[complex]])
        vector[vector[complex]] Zernike(int, int, double ,double, vector[vector[complex]])
        void test()
        double getGridSize()
        void setGridSize(double newGridSize)
        double getWavelength()
        void setWavelength(double newWavelength)
        int getGridDimension()
     
cdef class Init:
    """
        LP = LightPipes.Init()
            Initiates the LightPipes for Python optical toolbox.

        Example::

            >>> import LightPipes
            >>> LP = LightPipes.Init()
            >>> LP.version()
            version = 1.0.7
            >>> F = LP.Begin(0.03, 500e-9, 500)
            >>> F = LP.CircAperture(0.005,0,0,F)
                  .
                  .
                  .

    """
    
    cdef lpspy *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self):
        self.thisptr = new lpspy()
    def __dealloc__(self):
        del self.thisptr
    def Axicon(self, phi, n1, x_shift, y_shift, Fin):
        """
        Fout = Axicon(phi, n1, x_shift, y_shift, Fin)             
            Propagates the field through an axicon.

        Args::
        
            phi: top angle of the axicon in radians
            n1: refractive index of the axicon material
            x_shift, y_shift: shift from the center
            Fin: input field
            
        Returns::
          
            Fout: output field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Bessel beam with axicon <BesselBeam>`

        """
        return self.thisptr.Axicon(phi, n1, x_shift, y_shift, Fin)
    def BeamMix(self, Fin1, Fin2):
        """
        Fout = BeamMix(F1, F2)             
            Addition of the fields F1 and F2.

        Args::
        
            F1, F2: input fields
            
        Returns::
          
            Fout: output field (N x N square array of complex numbers).
            
        Example:
        
        :ref:`Two holes interferometer <Young>`
        
        """
        return self.thisptr.BeamMix(Fin1, Fin2)
    def Begin(self,size,labda,N):
        """
        F = Begin(GridSize, Wavelength, N)             
            Creates a plane wave (phase = 0.0, amplitude = 1.0)

        Args::
        
            GridSize: size of the grid
            Wavelength: wavelength of the field
            N: N x N grid points (N must be even)
            
        Returns::
         
            F: N x N square array of complex numbers (1+0j).
                
        Example:
        
        :ref:`Diffraction from a circular aperture <Diffraction>`
        
        """
        return self.thisptr.Begin(size, labda, N)
    def CircAperture(self, R, x_shift, y_shift, Fin):
        """
        Fout = CircAperture(R, x_shift, y_shift, Fin)             
            Propagates the field through a circular aperture.

        Args::
        
            R: radius of the aperture
            x_shift, y_shift: shift from the center
            Fin: input field
            
        Returns::
         
            Fout: output field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Diffraction from a circular aperture <Diffraction>`
        
        """
        return self.thisptr.CircAperture(R, x_shift, y_shift, Fin)
    def CircScreen(self, R, x_shift, y_shift, Fin):
        """
        Fout = CircScreen(R, x_shift, y_shift, Fin)             
            Diffracts the field by a circular screen.

        Args::
        
            R: radius of the screen
            x_shift, y_shift: shift from the center
            Fin: input field
            
        Returns::
         
            Fout: output field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Spot of Poisson <Poisson>`
        
        """
        return self.thisptr.CircScreen(R, x_shift, y_shift, Fin)
    def Convert(self, Fin):
        """
        Fout = Convert(Fin)             
            Converts the field from a spherical variable coordinate to a normal coordinate system.

        Args::
        
            Fin: input field
            
        Returns::
         
            Fout: output field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Unstable resonator <Unstab>`
        
        """
        return self.thisptr.Convert( Fin)
    def Forvard(self, z, Fin):
        """
        Fout = Forvard(z, Fin)             
            Propagates the field using a FFT algorithm.

        Args::
        
            z: propagation distance
            Fin: input field
            
        Returns::
         
            Fout: output field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Diffraction from a circular aperture <Diffraction>`
        
        """
        return self.thisptr.Forvard(z, Fin)                    
    def Fresnel(self, z, Fin):
        """
        Fout = Fresnel(z, Fin)             
            Propagates the field using a convolution method.

        Args::
        
            z: propagation distance
            Fin: input field
            
        Returns::
         
            Fout: output field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Two holes interferometer <Young>`

        """
        return self.thisptr.Fresnel(z, Fin)  
    def Gain(self, Isat, alpha0, Lgain, Fin):
        """
        Fout = Gain(Isat, alpha0, Lgain, Fin)             
            Propagates the field through a thin saturable gain sheet.
            
            :math:`F_{out}(x,y) = F_{in}(x,y) e^{\\alpha L_{gain}}`, with
            :math:`\\alpha = \\dfrac{\\alpha_0}{1 + {2 I(x,y)}/{I_{sat}}}`.
             
            :math:`2\\alpha L_{gain}` is the net round-trip intensity gain. 
            :math:`\\alpha_0` is the small-signal intensity gain and 
            :math:`I_{sat}` is the saturation intensity of the gain medium 
            with a length :math:`L_{gain}`.
            
            The intensity must be doubled because of the left- and right 
            propagating fields in a normal resonator. (If only one field is propagating in one direction (ring 
            laser) you should double :math:`I_{sat}` as well to remove the factor 2 in the denominator).

            The gain sheet should be at one of the mirrors of a (un)stable laser resonator.
            
            See: Rensch and Chester (1973).
            
        Args::
        
            Isat: saturation intensity
            alpha0: small signal gain
            Lgain: length of the gain sheet
            Fin: input field
            
        Returns::
         
            Fout: output field (N x N square array of complex numbers).

        Example:
        
        :ref:`Unstable resonator <Unstab>`

        """
        return self.thisptr.Gain(Isat, alpha0, Lgain, Fin)
    def GaussAperture(self, w, x_shift, y_shift, T, Fin):
        """
        Fout = GaussAperture(w, x_shift, y_shift, T, Fin)
            Inserts an aperture with a Gaussian shape in the field.
        
            :math:`F_{out}(x,y)= \\sqrt{T}e^{ -\\frac{ x^{2}+y^{2} }{2w^{2}} } F_{in}(x,y)`

        Args::
        
            w: 1/e intensity width
            x_shift, y_shift: shift from center
            T: center intensity transmission
            Fin: input field
        
        Returns::
        
            Fout: output field (N x N square array of complex numbers).

        """   
        return self.thisptr.GaussAperture( w, x_shift, y_shift, T, Fin)
    def GaussScreen(self, w, x_shift, y_shift, T, Fin):
        """
        Fout = GaussScreen(w, x_shift, y_shift, T, Fin)
            Inserts an screen with a Gaussian shape in the field.
    
            :math:`F_{out}(x,y)= \\sqrt{1-(1-T)e^{ -\\frac{ x^{2}+y^{2} }{w^{2}} }} F_{in}(x,y)`

       Args::
        
            w: 1/e intensity width
            x_shift, y_shift: shift from center
            T: center intensity transmission
            Fin: input field
        
        Returns::
        
            Fout: output field (N x N square array of complex numbers).

        """   
        return self.thisptr.GaussScreen( w, x_shift, y_shift, T, Fin)
    def GaussHermite(self, m, n, A, w0, Fin):
        """
        Fout = GaussHermite(m, n, A, w0, Fin)
            Substitutes a Gauss-Hermite :math:`TEM_{m,n}` mode (beam waist) in the field.
    
            :math:`F_{m,n}(x,y,z=0) = A H_m\\left(\\dfrac{\\sqrt{2}x}{w_0}\\right)H_n\\left(\\dfrac{\\sqrt{2}y}{w_0}\\right)e^{-\\frac{x^2+y^2}{w_0^2}}`

        Args::
            
            m, n: mode indices
            A: Amplitude
            w0: Guaussian spot size parameter in the beam waist (1/e amplitude point)
            Fin: input field
            
        Returns::
        
            Fout: output field (N x N square array of complex numbers).            
            
        Reference::
        
            A. Siegman, "Lasers", p. 642

        """
        return self.thisptr.GaussHermite( m, n, A, w0, Fin)
    def GaussLaguerre(self, p, m, A, w0, Fin):
        """
        Fout = GaussLaguerre(p, m, A, w0, Fin)
            Substitutes a Gauss-Laguerre :math:`TEM_{p,m}` mode (beam waist) in the field.
    
            :math:`F_{p,m}(x,y,z=0) = A \\left(\\frac{\\rho}{2}\\right)^{\\frac{|m|}{2} }L^p_m\\left(\\rho\\right)e^{-\\frac{\\rho}{2}}\\cos(m\\theta)`,
            
            with :math:`\\rho=\\frac{2(x^2+y^2)}{w_0^2}`

        Args::
            
            p, m: mode indices
            A: Amplitude
            w0: Guaussian spot size parameter in the beam waist (1/e amplitude point)
            Fin: input field
            
        Returns::
        
            Fout: output field (N x N square array of complex numbers).            
            
        Reference::
        
            A. Siegman, "Lasers", p. 642

        """
            
        return self.thisptr.GaussLaguerre( p, m, A, w0, Fin)
    def IntAttenuator(self, att, Fin):
        """
        Fout = IntAttenuator(att, Fin)
            Attenuates the intensity of the field Fin by a factor :math:`att`
            
            :math:`F_{out}(x,y)=\\sqrt{att}F_{in}(x,y)`
            
        Args::
        
            att: intensity attenuation factor
            Fin: input field
            
        Returns::
        
            Fout: output field (N x N square array of complex numbers).
   
        """    
        return self.thisptr.IntAttenuator( att, Fin)                          
    def Lens(self, f, x_shift, y_shift, Fin):
        """
        Fout = Lens(f, x_shift, y_shift, Fin)
            Propagates the field through an ideal, thin lens.
            It adds a phase given by:
            :math:`F_{out}(x,y)=e^{-j\\frac{2\\pi}{\\lambda}\\left(\\frac{(x-x_{shift})^2+(y-y_{shift})^2}{2f}\\right)}F_{in}(x,y)`

       Args::
        
            f: focal length
            x_shift, y_shift: shift from center
            Fin: input field
            
        Returns::
        
            Fout: output field (N x N square array of complex numbers).

        """
        return self.thisptr.Lens(f, x_shift, y_shift, Fin)
    def LensForvard(self, f, z, Fin):
        return self.thisptr.LensForvard(f, z, Fin)
    def LensFresnel(self, f, z, Fin):
        return self.thisptr.LensFresnel(f, z, Fin)
    def MultIntensity(self, Intens, Fin):    
        return self.thisptr.MultIntensity( Intens, Fin)
    def MultPhase(self, Phase, Fin):    
        return self.thisptr.MultPhase( Phase, Fin)
    def Normal(self, Fin):    
        return self.thisptr.Normal(Fin)        
    def Intensity(self,flag,Fin):
        """
        I=Intensity(flag,Fin)
            Calculates the intensity, :math:`I(x,y)` of the field :math:`F_{in}(x,y)`
        
        :math:`I(x,y)=F_{in}(x,y).F_{in}(x,y)^*`
        
        Args::
        
            flag: 0= no normalization, 1=normalized to 1, 2=normalized to 255 (for bitmaps)
            Fin: input field
            
        Returns::
        
            I: intensity distribution (N x N square array of doubles)

        """
        return self.thisptr.Intensity(flag,Fin)                
    def Interpol(self, new_size, new_number, x_shift, y_shift, angle, magnif, Fin):
        return self.thisptr.Interpol(new_size, new_number, x_shift, y_shift, angle, magnif, Fin)
    def Phase(self,Fin):
        return self.thisptr.Phase(Fin)
    def PhaseUnwrap(self,Phi):
        return self.thisptr.PhaseUnwrap(Phi)        
    def PipFFT(self, index, Fin):    
        return self.thisptr.PipFFT(index, Fin)
    def Power(self, Fin):    
        return self.thisptr.Power(Fin)
    def RandomIntensity(self, seed, noise, Fin):    
        return self.thisptr.RandomIntensity(seed, noise, Fin)
    def RandomPhase(self, seed, maxPhase, Fin):    
        return self.thisptr.RandomPhase(seed, maxPhase, Fin)                
    def RectAperture(self, sx, sy, x_shift, y_shift, angle, Fin):    
        return self.thisptr.RectAperture(sx, sy, x_shift, y_shift, angle, Fin)
    def RectScreen(self, sx, sy, x_shift, y_shift, angle, Fin):    
        return self.thisptr.RectScreen(sx, sy, x_shift, y_shift, angle, Fin)
    def Steps(self, z, nstep, refr, Fin):
        """
        Fout = Steps(z, nstep, refr, Fin)             
            Propagates the field a distance, z, in nstep steps in a
            medium with a complex refractive index stored in the
            square array refr.

        Args::
        
            z: propagation distance
            nstep: number of steps
            refr: N x N array of complex numbers
            Fin: input field
            
        Returns::
          
            Fout: ouput field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Focus of a lens <FocLens>`

        """
        return self.thisptr.Steps(z, nstep, refr, Fin)  
    def Strehl(self, Fin):    
        return self.thisptr.Strehl(Fin)
    def SubIntensity(self, Intens, Fin):    
        return self.thisptr.SubIntensity( Intens, Fin)
    def SubPhase(self, Phase, Fin):    
        return self.thisptr.SubPhase( Phase, Fin)       
    def Tilt(self, tx, ty, Fin):    
        return self.thisptr.Tilt( tx, ty, Fin)  
    def Zernike(self, n, m, R, A, Fin):
        """
        Fout = Zernike(n, m, R, A, Fin)
            Substitutes a Zernike aberration phase distribution in the
            field.
            
            :math:`F_{out}(x,y)=e^{\\phi^m_n (x,y)}F_{in}(x,y)`
            
            with:
            
            :math:`\\phi^m_n(x,y)=-j \\frac{2 \\pi }{ \\lambda } Z^m_n {(\\rho (x,y) ,\\theta (x,y)) }`
            
            :math:`\\rho(x,y)=  \\sqrt{ \\frac{x^2+y^2}{R^2} }`
            
            :math:`\\theta (x,y)=atan \\big( \\frac{y}{x} \\big)`
            
            :math:`Z^m_n(\\rho , \\theta)=A \\sqrt{ \\frac{2(n+1)}{1+\\delta_{m0}} } V^m_n(\\rho)cos(m\\theta)`
            
            :math:`Z^{-m}_n(\\rho , \\theta)=A \\sqrt{ \\frac{2(n+1)}{1+\\delta_{m0}} }V^m_n(\\rho)sin(m\\theta)`
            
            :math:`V^m_n(\\rho)= \\sum_{s=0}^{ \\frac{n-m}{2} }  \\frac{(-1)^s(n-s)!}{s!( \\frac{n+m}{2}-s)!( \\frac{n-m}{2}-s )! } \\rho^{n-2s}`
            
            :math:`\\delta_{m0}= \\begin{cases}1 & m = 0\\\\0 & m  \\neq  0\\end{cases}`
            
           
        Args::
        
            n: radial order
            m: azimuthal order, n-|m| must be even, |m|<=n
            R: radius of the aberrated aperture
            A: size of the aberration
            Fin: input field
            
        Returns::
          
            Fout: ouput field (N x N square array of complex numbers).
                
        Example:
        
        :ref:`Zernike aberration <Zernike>`
        
        Reference: https://en.wikipedia.org/wiki/Zernike_polynomials
 

        """
        return self.thisptr.Zernike(n, m, R, A, Fin)
    def noll_to_zern(self,j):
        """
        Convert linear Noll index to tuple of Zernike indices.
        j is the linear Noll coordinate, n is the radial Zernike index and m is the azimuthal Zernike index.
        @param [in] j Zernike mode Noll index
        @return (n, m) tuple of Zernike indices
        @see <https://oeis.org/A176988>.
        Thanks to: Tim van Werkhoven, https://github.com/tvwerkhoven
        """
    
        if (j == 0):
            print("Noll indices start at 1, 0 is invalid.")
            return (0,0)
    
        n = 0
        j1 = j-1
        while (j1 > n):
            n += 1
            j1 -= n
    
        m = (-1)**j * ((n % 2) + 2 * int((j1+((n+1)%2)) / 2.0 ))
        return (n, m)
    def ZernikeNolltoMN(self,Noll):
        MN = []
        n = 0
        while (Noll > n):
            n += 1
            Noll -= n
        m = -n+2*Noll
        MN=[m,n]
        return MN
    def ZernikeName(self,Noll):
        if (Noll >= 1 and Noll <= 21):
            name = [
                "piston",
                "horizontal tilt",
                "vertical tilt",
                "defocus",
                "oblique primary astigmatism",
                "vertical primary astigmatism",
                "vertical coma",
                "horizontal coma",
                "vertical trefoil",
                "oblique trefoil",
                "primary spherical",
                "vertical secondary astigmatism",
                "oblique secondary astigmatism",
                "vertical quadrafoil",
                "oblique quadrafoil",
                "horizontal secondary coma",
                "vertical secondary coma",
                "oblique secondary trefoil",
                "vertical secondary trefoil",
                "oblique pentafoil",
                "vertical pentafoil",
            ]
            return name[Noll-1]
        elif Noll < 1:
            print( "Error in ZernikeName(Noll): argument must be larger than 1")
            return ""
        else:
            return ""
    def LPtest(self):
        self.thisptr.test()
    def LPhelp(self):
        """
        Go to the LightPipes documentation website on:
        
        http://pythonhosted.org/LightPipes/

        """
        webbrowser.open_new("https://pythonhosted.org/LightPipes/")
    def getGridSize(self):
        return self.thisptr.getGridSize()        
    def setGridSize(self, newSize):
        self.thisptr.setGridSize(newSize)
    def getWavelength(self):
        return self.thisptr.getWavelength()
    def setWavelength(self, newWavelength):
        self.thisptr.setWavelength(newWavelength)
    def getGridDimension(self):
        return self.thisptr.getGridDimension()
