#!/usr/bin/env python

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from LightPipes import *

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Unstable resonator")

wavelength = 308*nm
size=14*mm
N=100
w=5.48*mm
f1=-10*m; f2=20*m; L=10*m; Isat=1.0; alpha=1e-4; Lgain=1e4;
tx=0.0; ty=0.00000;

f = Figure(figsize = (3,3), dpi=75)
canvas = FigureCanvasTkAgg(f, master=root)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

F=Begin(size,wavelength,N);
F=RandomIntensity(2,1,F)
F=RandomPhase(5,1,F);
def TheExample():
    global F
    w=float(scale_w.get())*mm
    F=RectAperture(w,w,0,0,0,F);   F=Gain(Isat,alpha,Lgain,F);
    F=LensFresnel(f1,L,F);   F=Gain(Isat,alpha,Lgain,F);
    F=LensFresnel(f2,L,F);
    F=Tilt(tx,ty,F);
    F=Interpol(size,N,0,0,0,1,F);
    F2=RectScreen(w,w,0,0,0,F);
    I=Intensity(0,F2)
    plt = f.add_subplot(111,navigate=False )
    plt.imshow(I); plt.axis('off')
    canvas.show()
    
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    #Fatal Python Error: PyEval_RestoreThread: NULL tstate

scale_w = Tk.Scale(orient='horizontal', label = 'w/mm', length = 300, from_=1.0, to=8.0, resolution = 0.1, var = w)

scale_w.pack()


scale_w.set(w/mm)


button = Tk.Button(master=root, width = 20, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

def task():
    TheExample()
    root.after(1, task)  # reschedule event in 2 seconds

root.after(1, task)
root.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
