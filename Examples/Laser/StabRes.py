#!/usr/bin/env python

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import math
import time
import numpy as np
import sys
from Tkinter import *

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
try:
	import LightPipes
except ImportError:
	print "LightPipes not present"
	exit()
root = Tk.Tk()
root.wm_title("Laser with stable resonator")

m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m
rad=1;
mrad=1e-3*rad;

LP=LightPipes.Init()
wavelength=10600*nm;
size=20*mm;
N=100;
Isat=131/cm/cm; alpha=0.0067/cm; Lgain=30*cm;

f1=2.0*m
f2=5*m

L=30*cm
T=1;
Reflect=0.9;
w0=3.0*mm
n=10;
tx=0.00*mrad;
ty=0.00*mrad;
xwire=10.0*mm
ywire=10.0*mm

f = Figure(figsize = (5,5), dpi=N)
canvas = FigureCanvasTkAgg(f, master=root)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
plt = f.add_subplot(211,navigate=False )
plt2=f.add_subplot(212,navigate=False )

F=LP.Begin(size,wavelength,N);
x=range(-N/2,N/2)
x=np.asarray(x)*size/N/mm
def TheExample():
	global F,f1,f2,L,w0
	w0=float(scale_w0.get())*mm
	xwire=float(scalexwire.get())*mm
	ywire=float(scaleywire.get())*mm
	f1=float(scale_f1.get()*cm)
	f2=float(scale_f2.get()*cm)
	L=float(scale_L.get())*cm

	F=LP.RandomIntensity(time.time(),1e-8,F)
	F=LP.CircAperture(w0,0,0,F)
	F=LP.RectScreen(size,0.2*mm,0.0,ywire,0.0,F)
	F=LP.RectScreen(0.2*mm,size,xwire,0.0,0.0,F)
	Iw=LP.Intensity(1,F)
	F=LP.Lens(f2,0,0,F);
	F=LP.Fresnel(L,F); F=LP.Gain(Isat,alpha,Lgain,F);
	F=LP.Lens(f1,0,0,F);
	F=LP.Fresnel(L,F); F=LP.Gain(Isat,alpha,Lgain,F);
	F=LP.IntAttenuator(Reflect,F)
	P=LP.Power(F)
	I=LP.Intensity(0,F)
	y=np.asarray(Iw[N/2])
	
	plt.clear()
	plt2.clear()
	g1=1-L/(2*f1);
	g2=1-L/(2*f2);
	g=g1*g2
	plt.text(0,-2,"E=%5.3f"% P)
	plt.text(100,-4,"g=%5.3f"% g)
	plt.imshow(Iw); plt.axis('off')
	plt2.plot(x,y)

	canvas.show()

def _quit():
	root.quit()		# stops mainloop
	root.destroy()	# this is necessary on Windows to prevent
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
	F=LP.GaussHermite(mode_m,mode_n,1,w0,F);
	#F=LP.GaussLaguerre(2,3,1,w0,F);
	F=LP.Forvard(z2,F);	

frame2=Frame(root)
frame2.pack(side=Tk.BOTTOM)
frame3=Frame(frame2)
frame3.pack(side=Tk.BOTTOM)
frame4=Frame(frame3)
frame4.pack(side=Tk.BOTTOM)

scalexwire = Tk.Scale(root, orient='horizontal', label = 'x-wire position/mm', length = 300, from_=-size/2/mm, to=size/2/mm, resolution = 0.001)
scalexwire.pack(side = Tk.LEFT)
scalexwire.set(xwire/mm)

scaleywire = Tk.Scale(root, orient='horizontal', label = 'y-wire position/mm', length = 300, from_=-size/2/mm, to=size/2/mm, resolution = 0.001)
scaleywire.pack(side = Tk.LEFT)
scaleywire.set(ywire/mm)

scale_w0 = Tk.Scale(frame2, orient='horizontal', label = 'w/mm', length = 300, from_=0.0, to=size/2/mm, resolution = 0.01)
scale_w0.pack(side = Tk.LEFT)
scale_w0.set(w0/mm)

scale_L = Tk.Scale(frame2, orient='horizontal', label = 'L/cm', length = 300, from_=10.0, to=500.0, resolution = 0.01)
scale_L.pack(side = Tk.LEFT)
scale_L.set(L/cm)

scale_f1 = Tk.Scale(frame3, orient='horizontal', label = 'f1/cm', length = 300, from_=100.0, to=500.0, resolution = 0.1)
scale_f1.pack(side = Tk.LEFT)
scale_f1.set(f1/cm)

scale_f2 = Tk.Scale(frame3, orient='horizontal', label = 'f2/cm', length = 300, from_=100.0, to=500.0, resolution = 0.1)
scale_f2.pack(side = Tk.LEFT)
scale_f2.set(f2/cm)

button = Tk.Button(frame4, width = 20, text='eigen mode', command=_eigenmode)
button.pack(side=Tk.LEFT)

order_m=Tk.Spinbox(frame4,width=1,from_=0, to=5)
order_m.pack(side=Tk.LEFT)

order_n=Tk.Spinbox(frame4,width=1,from_=0, to=5)
order_n.pack(side=Tk.LEFT)

button = Tk.Button(frame4, width = 20, text='Quit', command=_quit)
button.pack(side=Tk.LEFT)

def task():
    TheExample()
    root.after(1, task)  # reschedule event in 2 seconds

root.after(1, task)
root.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.

