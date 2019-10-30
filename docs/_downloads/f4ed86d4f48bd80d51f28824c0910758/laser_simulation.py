#!/usr/bin/env python
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
import time
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
root.wm_protocol("WM_DELETE_WINDOW", root.quit)
power=[]
roundtrip=0

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
dt=2*L/2.998*1e-8
fig=plt.figure(figsize=(6,9))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()
F=Begin(size,wavelength,N)

def TheExample():
    #start_time=time.time()
    global F,f1,f2,L,w0,roundtrip
    global Reflect
    w0=float(scale_w0.get())*mm/2
    xwire=float(scalexwire.get())*mm
    ywire=float(scaleywire.get())*mm
    f1=float(scale_f1.get()*cm)/2
    f2=float(scale_f2.get()*cm)/2
    L=float(scale_L.get())*cm
    Reflect=float(scale_Reflect.get())
    tx=-float(scale_tx.get())*mrad
    ty=float(scale_ty.get())*mrad
    alpha=float(scale_gain.get())/cm
    F=RandomIntensity(time.time(),1e-8,F)
    F=CircAperture(w0,0,0,F)
    F=RectScreen(size,0.2*mm,0.0,ywire,0.0,F)
    F=RectScreen(0.2*mm,size,xwire,0.0,0.0,F)
    Iw=Intensity(0,F)
    F=Lens(f2,0,0,F);
    F=Forvard(L,F); F=Gain(Isat,alpha,Lgain,F);
    F=Lens(f1,0,0,F);
    F=Tilt(tx,ty,F)
    F=Forvard(L,F); F=Gain(Isat,alpha,Lgain,F);
    F=IntAttenuator(Reflect,F)
    P=Power(F)*(1-Reflect)*size/N*size/N
    power.append(P); roundtrip=roundtrip+1

    if (roundtrip>500):
        power.pop(0)
    Iout=Isat*(alpha*Lgain-0.5*math.log(1/Reflect))*math.pi*w0*w0

    ax1.clear()
    ax2.clear()

    g1=1-L/(2*f1);
    g2=1-L/(2*f2);
    g=g1*g2
    v.set(  "Power=%5.3f W\n"% P+
            "g1 = %5.3f\n"%g1+
            "g2 = %5.3f\n"%g2+
            "g  = %5.3f\n"%g
            )
    ax1.imshow(Iw,cmap='rainbow'); ax1.axis('off'); ax1.axis('equal')
    ax1.set_title('laser mode') 
    ax2.plot(power); ax2.set_ylim(0,10); ax2.set_xlim(0,500)
    s='%3.1f ns/div'% (2.0*L/2.988*1000.0)
    ax2.set_xlabel(s); ax2.set_ylabel('power [W]')
    ax2.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',      # ticks along the bottom edge are off
        top='on',         # ticks along the top edge are off
        labelbottom='off')
    ax2.grid()
    canvas.show()
    #print("Execution time: --- %4.2f seconds ---" % (time.time() - start_time)) 

def _quit():
    root.quit()
    root.destroy()
    
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
    #F=GaussLaguerre(mode_m,mode_n,1,w0,F);
    F=Forvard(z2,F);

frame1=Frame(root)
frame1.pack(side=Tk.BOTTOM)
frame2=Frame(frame1)
frame2.pack(side=Tk.BOTTOM)
frame3=Frame(frame2)
frame3.pack(side=Tk.BOTTOM)
frame4=Frame(frame3)
frame4.pack(side=Tk.BOTTOM)
frame5=Frame(frame4)
frame5.pack(side=Tk.BOTTOM)
frame6=Frame(frame5)
frame6.pack(side=Tk.BOTTOM)
frame7=Frame(frame6)
frame7.pack(side=Tk.BOTTOM)

Label(root, textvariable=v).pack(side=Tk.LEFT)

scalexwire = Tk.Scale(frame1, orient='horizontal', label = 'x-wire position [mm]', length = 200, from_=-size/2/mm, to=size/2/mm, resolution = 0.001)
scalexwire.pack(side = Tk.LEFT)
scalexwire.set(xwire/mm)

scaleywire = Tk.Scale(frame1, orient='horizontal', label = 'y-wire position [mm]', length = 200, from_=-size/2/mm, to=size/2/mm, resolution = 0.001)
scaleywire.pack(side = Tk.LEFT)
scaleywire.set(ywire/mm)

scale_w0 = Tk.Scale(frame2, orient='horizontal', label = 'aperture diameter [mm]', length = 200, from_=0.0, to=size/mm, resolution = 0.01)
scale_w0.pack(side = Tk.LEFT)
scale_w0.set(2*w0/mm)

scale_Reflect = Tk.Scale(frame2, orient='horizontal', label = 'outcoupler reflection', length = 200, from_=0.0, to=1.0, resolution = 0.01)
scale_Reflect.pack(side = Tk.LEFT)
scale_Reflect.set(Reflect)

scale_f1 = Tk.Scale(frame3, orient='horizontal', label = 'mirror M1 radius [cm]', length = 200, from_=10.0, to=1000.0, resolution = 0.1)
scale_f1.pack(side = Tk.LEFT)
scale_f1.set(f1/cm)

scale_f2 = Tk.Scale(frame3, orient='horizontal', label = 'mirror M2 radius [cm]', length = 200, from_=10.0, to=1000.0, resolution = 0.1)
scale_f2.pack(side = Tk.LEFT)
scale_f2.set(f2/cm)

scale_L = Tk.Scale(frame4, orient='horizontal', label = 'resonator length [cm]', length = 200, from_=10.0, to=100.0, resolution = 0.01)
scale_L.pack(side = Tk.LEFT)
scale_L.set(L/cm)

scale_gain = Tk.Scale(frame4, orient='horizontal', label = 'gain [cm^-1]', length = 200, from_=0.0, to=0.01, resolution = 0.0001)
scale_gain.pack(side = Tk.LEFT)
scale_gain.set(alpha*cm)

scale_tx = Tk.Scale(frame5, orient='horizontal', label = 'mirror M2 x-tilt [mrad]', length = 200, from_=-10.0, to=10.0, resolution = 0.1)
scale_tx.pack(side = Tk.LEFT)
scale_tx.set(tx/mrad)

scale_ty = Tk.Scale(frame5, orient='horizontal', label = 'mirror M2 y-tilt [mrad]', length = 200, from_=-10.0, to=10.0, resolution = 0.1)
scale_ty.pack(side = Tk.LEFT)
scale_ty.set(ty/mrad)

button_eigenmode = Tk.Button(frame6, width = 18, text='eigen mode', command=_eigenmode)
button_eigenmode.pack(side=Tk.LEFT, pady=10)

order_m=Tk.Spinbox(frame6,width=1,from_=0, to=5)
order_m.pack(side=Tk.LEFT)

order_n=Tk.Spinbox(frame6,width=1,from_=0, to=5)
order_n.pack(side=Tk.LEFT, pady=10)

button_quit = Tk.Button(frame7, width = 24, text='Quit', command=_quit)
button_quit.pack(side=Tk.LEFT, pady=10)

def task():
    TheExample()
    root.after(1, task)

root.after(1, task)
root.mainloop()


