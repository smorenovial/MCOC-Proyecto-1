# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:14:40 2019

@author: piedi
"""

from matplotlib.pylab import *
from scipy.interpolate import interp1d
import numpy as np

 
a = 1.          #Ancho del dominio
b = 1.
c = 1.          #Largo del dominio
Nx = 30         #Numero de intervalos en x
Ny = 30  
Nz = 30 
       #Numero de intervalos en Y
 
dx = b / Nx     #Discretizacion espacial en X
dy = a / Ny     #Discretizacion espacial en Y
dz = c / Nz

h = dx    # = dy
 
 
if dx != (dy or dz) :
    print("ERRROR!!!!! dx != dy or dx!= dz")
    exit(-1)   #-1 le dice al SO que el programa fallo.....
 
#Funcion de conveniencia para calcular coordenadas del punto (i,j)
 
# def coords(i,j):
#   return dx*i, dy*j
# x, y = coords(4,2)  
 
# i, j = 4, 2 
# x, y = dx*i, dy*j
 
coords = lambda i, j : (dx*i, dy*j,dz*l)
#x, y,z = coords(6,4,2) 
 
#print "x = ", x
#print "y = ", y
#print "z = ", z

 
# Dado que la condicion inicial es que la temeperatura intera es de 20 grados celsius
# se crea una matriz con puros numeros 20 en su interior


u_k = 20*ones((Nx+1,Ny+1,Nz+1), dtype=double)#dtype es el tipo de datos (double, float, int32, int16...)
u_km1 = 20*ones((Nx+1,Ny+1,Nz+1), dtype=double)  #dtype es el tipo de datos (double, float, int32, int16...)
 
#CB esencial
# Se aplica las condiciones base del problema
u_k[0,:,:] = 20.
u_k[-1,:,:] = 20.

 
#Buena idea definir funciones que hagan el codigo expresivo
def printbien(u):
    print u.T[Nx::-1,:,:]
 
print u_k               #Imprime con el eje y invertido
printbien(u_k)
 
def imshowbien(u):
    imshow(u.T[Nx::-1,:,:])
    colorbar(extend='both',cmap='plasma')
   # clim(10, 30)   # Segun el video la barra de temperatura va de 10 a 30 grados celsius
 
#Parametros del problema (hierro)
dt = 1.0       # s
K = 79.5       # m^2 / s   
c = 450.       # J / kg C
rho = 7800.    # kg / m^3
alpha = K*dt/(c*rho*dx**2)
 
# dx =  0.166666666667
# dt = 1.0
# alpha =  0.000815384615385
 
alpha_bueno = 0.0001
dt = alpha_bueno*(c*rho*dx**2)/K
alpha = K*dt/(c*rho*dx**2)
 
 
#Informar cosas interesantes
print "dt = ", dt
print "dx = ", dx
print "K = ", K
print "c = ", c
print "rho = ", rho
print "alpha = ", alpha
 
k = 0
 
# figure(1)
# imshowbien(u_k)
# title("k = {}   t = {} s".format(k, k*dt))
# savefig("movie/frame_{0:04.0f}.png".format(k))
# close(1)
 
#Loop en el tiempo 
# Se fija un dnext_t igual a 1 para que vaya avanzando cada un minuto
dnext_t = 1   #  20.00
next_t = 0.
framenum = 0
graficocentro = []
# Se fija un valor de 60 de tal forma de que arroje mas imagenes

contador=0
lista=[]
lista2=[]
while contador<10:
    lista.append([1,1,1])
    contador+=1

for k in range(int32(11./dt)):
    t = dt*(k+1)
    print "k = ", k, " t = ", t
 
    #CB esencial
    # Se fijan las condiciones basales
    u_k[0,:,:] = 20.
    u_k[-1,:,:] = 20.
    
    print "Calor en punto [29,29,29]:", u_k[29,29,29]
    # Se fija la funcion de variacion de calor en la cara superior 
    u_k[:,-1,:] = 20 + 10* sin((2* math.pi/24)*t )

    numeros=[1,2,3,4,5,6,7,8,9,10]

    if k == 200: # Tiempo aproximado valor 1
        lista2.append(u_k[29,29,29])

    if k == 410: # Tiempo aproximado valor 2
        lista2.append(u_k[29,29,29])

    if k == 615: # Tiempo aproximado valor 3
        lista2.append(u_k[29,29,29])

    if k == 815: # Tiempo aproximado valor 4
        lista2.append(u_k[29,29,29])

    if k == 1015: # Tiempo aproximado valor 5
        lista2.append(u_k[29,29,29])

    if k == 1216: # Tiempo aproximado valor 6
        lista2.append(u_k[29,29,29])

    if k == 1417: # Tiempo aproximado valor 7
        lista2.append(u_k[29,29,29])

    if k == 1618: # Tiempo aproximado valor 8
        lista2.append(u_k[29,29,29])

    if k == 1819: # Tiempo aproximado valor 9
        lista2.append(u_k[29,29,29])

    if k == 2020: # Tiempo aproximado valor 10
        lista2.append(u_k[29,29,29])


    #Loop en el espacio   i = 1 ... n-1   u_km1[0] = 0  u_km1[n] = 20
    for i in range(1,Nx):
        for j in range(1,Ny):
            for l in range(1,Nz):
                
            #Algoritmo de diferencias finitas 2-D para difusion
 
            #Laplaciano
                nabla_u_k = (u_k[i-1,j,l] + u_k[i+1,j,l] + u_k[i,j-1,l] + u_k[i,j+1,l] + u_k[i,j,l-1] + u_k[i,j,l+1]- 6*u_k[i,j,l])/h**2
 
            #Forward euler..
                u_km1[i,j,l] = u_k[i,j,l] + alpha*nabla_u_k

                
    #CB natural
    u_km1[Nx,:,:] = u_km1[Nx-1,:,:]
    u_km1[:,Ny,:] = u_km1[:,Ny-1,:]
    u_km1[:,:,Nz] = u_km1[:,:,Nz-1]
    #Avanzar la solucion a k + 1
    u_k = u_km1
 
    #CB esencial una ultima vez
    # Nuevamente se fijas las condiciones bases y ademas se fija la funcion de variacion
    # de calor de la cara superior
    u_k[0,:,:] = 20.
    u_k[-1,:,:] = 20.
    u_k[:,-1,:] = 20 + 10* sin((2*math.pi/24)*t)
 
    print "Tmax = ", u_k.max()
 
print "Calores del punto [29,29,29], en funcion del tiempo (t):"
print lista2
print "Tiempos t:"
print numeros

x = np.linspace(0, 10, num=11, endpoint=True)
y = np.lista2(t)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=41, endpoint=True)
plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()



