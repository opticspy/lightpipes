# coding: utf-8
# diaprojector.py
# Phyton script voor het plotten van de meetresultaten van de diaprojector
# Fred van Goor, 25-11-2021
import matplotlib.pyplot as plt
import numpy as np

f=.107 #brandpuntsafstand van de lens [m]

data=np.loadtxt('meting.txt') #lees de meetresultaten 
v=data[0:,0] #voorwerpafstand [m]
b=data[0:,1] #beeldafstand [m]
V=-data[0:,2] #vergroting

#theorie formule afbeelding
vt=np.array([0.01, 100])
bt=vt*f/(vt - f) #theoretische beeldafstand
Vt=-bt/vt #theoretische vergroting

#Plot de metingen als rechte lijn
fig, ax = plt.subplots(nrows=1,ncols=2,constrained_layout=True)
ax[0].scatter(1/v, 1/b, marker='o') #plot meetresultaten (rechte lijn)
ax[0].plot(1/vt,1/bt,color='red') #plot theoretische waarden
ax[0].set(
        xlabel='1/v (1//m)', ylabel='1/b (1/m)',
        title='dia projector, f = '+ str(f) + ' m' ,
        xlim=(0,10), ylim=(0,10),
        )
ax[0].grid()
ax[0].set_aspect('equal')

ax[1].scatter(v,1/V) #plot vergroting (rechte lijn)
ax[1].plot(vt,1/Vt,color='red') #plot theoretische waarden
ax[1].set(
        xlabel='v (m)', ylabel='1/V (-)',
        title='dia projector, f = '+ str(f) + ' m' ,
        xlim=(0.1,0.3), ylim=(0,-1.2),
        )
fig.canvas.draw() #herteken de figuur
extent = ax[0].get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted())
fig.savefig('figure0.png', bbox_inches=extent) #output figuur 0
extent = ax[1].get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted())
fig.savefig('figure1.png', bbox_inches=extent) #output figuur 1
plt.show() #toon de figuur
