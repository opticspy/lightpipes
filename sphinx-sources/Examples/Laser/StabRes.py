#!/usr/bin/env python
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import math
import time
import numpy as np
import sys

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
else:
    from tkinter import *
    import tkinter as Tk

from LightPipes import *

root = Tk.Tk()
root.wm_title("Laser with stable resonator")

wavelength=10600*nm;
size=20*mm;
N=100; N2=int(N/2)
Isat=131*W/cm/cm; alpha=0.0067/cm; Lgain=30*cm;

f1=2.0*m
f2=5*m

L=30*cm
T=1;
Reflect=0.9;
w0=2.4*mm
n=10;
tx=0.00*mrad;
ty=0.00*mrad;
xwire=10.0*mm
ywire=10.0*mm

f = Figure(figsize = (10,4), dpi=N)
canvas = FigureCanvasTkAgg(f, master=root)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
plt = f.add_subplot(211,navigate=False )
plt2=f.add_subplot(212,navigate=False )

F=Begin(size,wavelength,N);
x=range(-N2,N2)
x=np.asarray(x)*size/N/mm
def TheExample():
    global F,f1,f2,L,w0
    w0=float(scale_w0.get())*mm/2
    xwire=float(scalexwire.get())*mm
    ywire=float(scaleywire.get())*mm
    f1=float(scale_f1.get()*cm)/2
    f2=float(scale_f2.get()*cm)/2
    L=float(scale_L.get())*cm
    Reflect=float(scale_Reflect.get())
    tx=-float(scale_tx.get())*mrad
    ty=float(scale_ty.get())*mrad
    
    F=RandomIntensity(time.time(),1e-8,F)
    F=CircAperture(w0,0,0,F)
    F=RectScreen(size,0.2*mm,0.0,ywire,0.0,F)
    F=RectScreen(0.2*mm,size,xwire,0.0,0.0,F)
    Iw=Intensity(0,F)
    F=Lens(f2,0,0,F);
    F=Fresnel(L,F); F=Gain(Isat,alpha,Lgain,F);
    F=Lens(f1,0,0,F);
    F=Tilt(tx,ty,F)
    F=Fresnel(L,F); F=Gain(Isat,alpha,Lgain,F);
    F=IntAttenuator(Reflect,F)
    P=Power(F)*(1-Reflect)*size/N*size/N  
    #I=LP.Intensity(0,F)
    y=np.asarray(Iw[N2])
    #Iout=Isat*(alpha*Lgain-0.5*math.log(1/Reflect))*math.pi*w0*w0
    plt.clear()
    plt2.clear()
    g1=1-L/(2*f1);
    g2=1-L/(2*f2);
    g=g1*g2
    plt.text(0,-5,"Power=%5.3f W"% P)
    plt.text(150,-5,"g1=%5.3f"% g1)
    plt.text(150,15,"g2=%5.3f"% g2)
    plt.text(150,35,"g=%5.3f"% g)
    plt.imshow(Iw); plt.axis('off')
    plt2.plot(x,y)
    canvas.show()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstat
def _eigenmode():
    global F,f1,f2,L,w0
    g1=1-L/(2*f1);
    g2=1-L/(2*f2);
    g=g1*g2
    z1=L*g2*(1-g1)/(g1+g2-2*g1*g2);
    z2=L-z1;
    if (g>0):
        w0=math.sqrt(wavelength*L/math.pi)*(g1*g2*(1-g1*g2)/(g1+g2-2*g1*g2)**2)**0.25;
    mode_m=int(order_m.get())
    mode_n=int(order_n.get())
    
    F=GaussHermite(mode_m,mode_n,1,w0,F);
    #F=GaussLaguerre(2,3,1,w0,F);
    F=Forvard(z2,F);

frame2=Frame(root)
frame2.pack(side=Tk.BOTTOM)
frame3=Frame(frame2)
frame3.pack(side=Tk.BOTTOM)
frame4=Frame(frame3)
frame4.pack(side=Tk.BOTTOM)
frame5=Frame(frame4)
frame5.pack(side=Tk.BOTTOM)

scalexwire = Tk.Scale(root, orient='horizontal', label = 'x-wire position [mm]', length = 300, from_=-size/2/mm, to=size/2/mm, resolution = 0.001)
scalexwire.pack(side = Tk.LEFT)
scalexwire.set(xwire/mm)

scaleywire = Tk.Scale(root, orient='horizontal', label = 'y-wire position [mm]', length = 300, from_=-size/2/mm, to=size/2/mm, resolution = 0.001)
scaleywire.pack(side = Tk.LEFT)
scaleywire.set(ywire/mm)

scale_w0 = Tk.Scale(frame2, orient='horizontal', label = 'aperture diameter [mm]', length = 300, from_=0.0, to=size/mm, resolution = 0.01)
scale_w0.pack(side = Tk.LEFT)
scale_w0.set(2*w0/mm)

scale_L = Tk.Scale(frame2, orient='horizontal', label = 'resonator length [cm]', length = 200, from_=10.0, to=100.0, resolution = 0.01)
scale_L.pack(side = Tk.LEFT)
scale_L.set(L/cm)

scale_Reflect = Tk.Scale(frame2, orient='horizontal', label = 'outcoupler reflection', length = 200, from_=0.0, to=1.0, resolution = 0.01)
scale_Reflect.pack(side = Tk.LEFT)
scale_Reflect.set(Reflect)

scale_f1 = Tk.Scale(frame3, orient='horizontal', label = 'mirror M1 radius [cm]', length = 300, from_=10.0, to=1000.0, resolution = 0.1)
scale_f1.pack(side = Tk.LEFT)
scale_f1.set(f1/cm)

scale_f2 = Tk.Scale(frame3, orient='horizontal', label = 'mirror M2 radius [cm]', length = 300, from_=10.0, to=1000.0, resolution = 0.1)
scale_f2.pack(side = Tk.LEFT)
scale_f2.set(f2/cm)

scale_tx = Tk.Scale(frame4, orient='horizontal', label = 'mirror M2 x-tilt [mrad]', length = 300, from_=-10.0, to=10.0, resolution = 0.1)
scale_tx.pack(side = Tk.LEFT)
scale_tx.set(tx/mrad)

scale_ty = Tk.Scale(frame4, orient='horizontal', label = 'mirror M2 y-tilt [mrad]', length = 300, from_=-10.0, to=10.0, resolution = 0.1)
scale_ty.pack(side = Tk.LEFT)
scale_ty.set(ty/mrad)

button = Tk.Button(frame5, width = 20, text='eigen mode', command=_eigenmode)
button.pack(side=Tk.LEFT)

order_m=Tk.Spinbox(frame5,width=1,from_=0, to=5)
order_m.pack(side=Tk.LEFT)

order_n=Tk.Spinbox(frame5,width=1,from_=0, to=5)
order_n.pack(side=Tk.LEFT)

button = Tk.Button(frame5, width = 20, text='Quit', command=_quit)
button.pack(side=Tk.LEFT)

def task():
    TheExample()
    root.after(1, task)  # reschedule event in 2 seconds

root.after(1, task)
root.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
