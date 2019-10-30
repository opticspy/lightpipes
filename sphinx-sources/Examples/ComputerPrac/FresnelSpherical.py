#!/usr/bin/env python
"""
    Computer practical 6.2. Fresnel diffraction, spherical wavefront.
    =================================================================

    This is part of the 'computer practical' set of assignments.
    Demonstrates Fresnel diffraction when a spherical wavefront enters 
    a round hole.
    Measure the values of z1, z2 and d for which minima and/or maxima on-axis occur
    and apply the Fresnel-zone theory to find the wavelength of the light.
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import math
import webbrowser

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
else:
    from tkinter import *
    import tkinter as Tk
from LightPipes import *

root = Tk.Tk()
root.wm_title("Computer practical: 6.2 Fresnel spherical wavefront.        LP-version = " + LPversion)
root.wm_protocol("WM_DELETE_WINDOW", root.quit)

wavelength=493*nm
size=5*mm
N=200;N2=int(N/2)

z1=50*cm
z2=20*cm
R=0.5*mm

D=DoubleVar()
Z1=DoubleVar()
Z2=DoubleVar()
D.set(2*R/mm)
Z1.set(z1/cm)
Z2.set(z2/cm)

fig=plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()

def TheExample(event):
    global I
    F=Begin(size,wavelength,N)
    F=GaussHermite(0,0,1.0,size/3,F)
    z1=Z1.get()*cm
    z2=Z2.get()*cm
    R=D.get()/2*mm
    F=CircAperture(R,0,0,F)
    F=Lens(-z1,0,0,F)
    FN=2/wavelength*(math.sqrt(z2*z2+R*R)-z2)
    if (FN >= 15.0):
        F=Forvard(z2,F)
    else:
        F=Fresnel(z2,F)
    I=Intensity(0,F)
 
    ax1.clear()
    ax1.contourf(I,50,cmap='hot'); ax1.axis('off'); ax1.axis('equal')
    str='Intensity distribution\ncenter-irradiance = %3.3f [a.u.]' %I[N2][N2]
    ax1.set_title(str) 
    canvas.draw()

def motion(event):
    x=event.xdata;y=event.ydata
    if (x and y is not None and x>0 and x<N and y>0 and y<N):
        v.set('x=%3.2f mm, y=%3.2f mm\n I=%3.3f [a.u.]' %((-size/2+x*size/N)/mm,(-size/2+y*size/N)/mm,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')

def openbrowser(event):
    webbrowser.open_new(r"https://opticspy.github.io/lightpipes/FresnelDiffraction.html")

def _quit():
    root.quit()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'diameter aperture [mm]',
        length = 200, from_=0.5, to=size/2/mm,
        resolution = 0.001,
        variable = D,
        cursor="hand2",
        command = TheExample).pack()

Scale(  root,
        orient='horizontal',
        takefocus = 1,
        label = 'z1 [cm]',
        length = 200,
        from_=0.01, to=200.0,
        resolution = 0.01,
        variable = Z1,
        cursor="hand2",
        command = TheExample).pack()

Scale(  root,
        orient='horizontal',
        takefocus = 1,
        label = 'z2 [cm]',
        length = 200,
        from_=0.01, to=200.0,
        resolution = 0.01,
        variable = Z2,
        cursor="hand2",
        command = TheExample).pack()

Button( root,
        width = 24,
        text='Quit',
        cursor="hand2",
        command=_quit).pack(pady=10)

link = Label(root, text="help", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", openbrowser)

Label(root, textvariable=v).pack(pady=50)

cid = fig.canvas.mpl_connect('motion_notify_event', motion)

TheExample(0)
root.mainloop()
root.destroy()

