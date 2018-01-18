#!/usr/bin/env python
"""
    Computer practical 4. Newton rings.
    ====================================================================

    This is part of the 'computer practical' set of assignments.
    Demonstrates the Newton rings experiment.
    Measure the diameter of the rings and find the radius of curvature
    of the lens. Find the refractive index of the medium between the lens and the plate.
    
    ..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
    
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import webbrowser
import numpy as np

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
    import tkMessageBox
else:
    from tkinter import *
    import tkinter as Tk
    from tkinter import messagebox
from LightPipes import *
import math

root = Tk.Tk()
root.wm_title("Computer practical: 4. Newton rings.        LP-version = " + LPversion)
root.wm_protocol("WM_DELETE_WINDOW", root.quit)

labda=530*nm;
size=5*mm;
N=300

R=150*cm


nfilm = 1.0

LABDA=DoubleVar()
NFILM=DoubleVar()
LABDA.set(labda/nm)
NFILM.set(nfilm)

fig=plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()

d=np.ndarray((N,N))
X=np.arange(-size/2,size/2,size/N)
Y=X

for i in range(0, N-1):
    for j in range(0, N-1):
        r2 = X[i]*X[i] + Y[j]*Y[j]
        d[i][j] = r2 / 2 / R
        
def TheExample(event):
    global I
    labda=LABDA.get()*nm
    nf=NFILM.get()
    F=Begin(size,labda,N);
    F1 = F
    Phi = Phase(F);
    k = 2 * math.pi / labda;
    p2 = 2 * nf * k;
    for i in range(1, N):
        for j in range(1, N):
            Phi[i][j] = p2 * d[i][j] + math.pi
    F = SubPhase(Phi, F);
    F = BeamMix(F1, F);
    I = Intensity(1, F);
    ax1.clear()
    ax1.imshow(I,cmap='hot')
    ax1.axis('off'); ax1.axis('equal');
    str='Intensity distribution'
    ax1.set_title(str)
    canvas.show()

def motion(event):
    x=event.xdata;y=event.ydata
    if (x and y is not None and x>0 and x<N and y>0 and y<N):
        v.set('x=%3.2f mm, y=%3.2f mm\n I=%3.3f [a.u.]' %((-size/2+x*size/N)/mm,(-size/2+y*size/N)/mm,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')

def _quit():
    root.quit()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'wavelength [nm]',
        length = 200, from_=300.0, to=1000.0,
        resolution = 0.1,
        variable = LABDA,
        cursor="hand2",
        command = TheExample).pack()

def cb():
    TheExample(0)
    
def openbrowser(event):
    webbrowser.open_new(r"https://opticspy.github.io/lightpipes/NewtonRings.html")
    
Checkbutton(root,
            text="insert medium between lens and plate",
            onvalue=1.74,
            offvalue=1.0,
            variable=NFILM,
            cursor="hand2",
            command = cb).pack()

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

