#!/usr/bin/env python
"""
    Computer practical 1. Spherical wavefront.
    =========================================================

    This is part of the 'computer practical' set of assignments.
    Demonstrates a spherical wavefront and the inverse quadratic dependency.
    Show in a graph whether or not the inverse square irradiance law holds.
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import webbrowser

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
else:
    from tkinter import *
    import tkinter as Tk
from LightPipes import *

root = Tk.Tk()
root.wm_title("Computer practical: 1. Spherical wavefront.        LP-version = " + LPversion)
root.wm_protocol("WM_DELETE_WINDOW", root.quit)

wavelength=500*nm
size=5*mm
N=200

z=20*cm
R=0.5*mm

D=DoubleVar()
Z=DoubleVar()
D.set(2*R/mm)
Z.set(z/cm)

fig=plt.figure(figsize=(6,4))
ax1 = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()

def TheExample(event):
    global I
    F=Begin(size,wavelength,N)
    z=Z.get()*cm
    R=D.get()/2*mm
    F=CircAperture(R,0,0,F)
    FN=R*R/z/wavelength
    if (FN >= 15.0):
        F=Forvard(z,F)
    else:
        F=Fresnel(z,F)
    I=Intensity(0,F)
    ax1.clear()
    ax1.contourf(I,50,cmap='hot'); ax1.axis('off'); ax1.axis('equal')
    ax1.set_title('Intensity distribution') 
    canvas.show()

def motion(event):
    x=event.xdata;y=event.ydata
    if (x is not None and y is not None and 0<x<N and 0<y<N):
        v.set('x=%3.2f mm, y=%3.2f mm\n I=%3.3f [a.u.]' %((-size/2+x*size/N)/mm,(-size/2+y*size/N)/mm,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')

def openbrowser(event):
    webbrowser.open_new(r"https://opticspy.github.io/lightpipes/SphericalWavefront.html")

def _quit():
    root.quit()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'diameter aperture [mm]',
        length = 200,
        from_=0.5, to=size/2/mm,
        resolution = 0.001,
        variable = D,
        cursor="hand2",
        command = TheExample).pack()


Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'z [cm]',
        length = 200,
        from_=0.01, to=200.0,
        resolution = 0.01,
        variable = Z,
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

Label(root, textvariable=v).pack()

cid = fig.canvas.mpl_connect('motion_notify_event', motion)

TheExample(0)
root.mainloop()
root.destroy()

