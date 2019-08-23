from matplotlib.pylab import *
from matplotlib import pyplot
from scipy.interpolate import interp1d
import numpy as np
import math

 
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

dt = 1.       # hr
K = 79.5       # m^2 / s   
c = 450.       # J / kg C
rho = 7800.    # kg / m^3
alpha = K*dt/(c*rho*dx**2)
C3s = 121       # kg
C2s = 44        # kg
C3A = 26.4      # kg
C4AF = 19.8     # kg
SO3 = 1.1       # kg
FreeCa = 2.75   # kg
Mgo = 4.95      # Kg
Slag = 0        # Kg
Hcem = 500*C3s+260*C2s+866*C3A+420*C4AF+624*SO3+1186*FreeCa+850*Mgo
Hu = Hcem*220 + 461*Slag + 1800 * 0.070345
  
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


# Se crean las listas que contendran la temperatura de cada sensor en un punto en especifico, en cada tiempo
sensor1=[]
sensor2=[]
sensor3=[]
sensor4=[]
sensor5=[]
sensor6=[]
sensor7=[]
sensor8=[]
sensor9=[]
# lista de cantidad de tiempos que se toman para graficar
numeros=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# lista para guardar cada uno de los valores de Q dependiendo del tiempo 
valoresQ=[]

# Ciclo que va guardando en la lista valoresQ el calor generado en cada tiempo por el fraguado del hormigon
contador=1
while contador<=20:
Qm= Hu * 220 * ((15.0/contador)**0.781429) * (0.781429/contador) * 0.75 * exp(-(15.0/contador)**0.781429) * exp(27.8284/8.314472*(1/(273+79)-1/(273+21)))
Qmodificado= Qm*(10**-6)
valoresQ.append(Qmodificado)
contador+=1


for k in range(int32(20./dt)):
    t = dt*(k+1)
    print "k = ", k, " t = ", t

    
    #CB esencial
    # Se fijan las condiciones basales

    

    # Se fija la funcion de variacion de calor en la cara superior 
    u_k[:,-1,:] = 20 + 10* sin((2* math.pi/24)*t )



    # Cada 202 veces que avanza k, sube en 1 el valor de t aproximadamente, por lo tanto
    # se asocia cada tiempo de 1 a 20 en este caso, con un k especifico



    if k == 200: # Tiempo aproximado valor 1
        matrizq= valoresQ[0]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k+= matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9



    if k == 410: # Tiempo aproximado valor 2

    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[0]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[1]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 615: # Tiempo aproximado valor 3
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[1]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[2]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 815: # Tiempo aproximado valor 4
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[2]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[3]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 1015: # Tiempo aproximado valor 5
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[3]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[4]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 1216: # Tiempo aproximado valor 6
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[4]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[5]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 1417: # Tiempo aproximado valor 7
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[5]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[6]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 1618: # Tiempo aproximado valor 8
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[6]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[7]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 1819: # Tiempo aproximado valor 9
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[7]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[8]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 2020: # Tiempo aproximado valor 10
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[8]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[9]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 2221: # Tiempo aproximado valor 11
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[9]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[10]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 2422: # Tiempo aproximado valor 12
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[10]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[11]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 2623: # Tiempo aproximado valor 13
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[11]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[12]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 2824: # Tiempo aproximado valor 14
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[12]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[13]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 3025: # Tiempo aproximado valor 15
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[13]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[14]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 3226: # Tiempo aproximado valor 16
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[14]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[15]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9

    if k == 3427: # Tiempo aproximado valor 17
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[15]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[16]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 3628: # Tiempo aproximado valor 18
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[16]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[17]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 3829: # Tiempo aproximado valor 19
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[17]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[18]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    if k == 4030: # Tiempo aproximado valor 20
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
        matrizq= valoresQ[18]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        matrizq1= valoresQ[19]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
        u_k=u_k+matrizq1-matrizq
        sensor4.append(u_k[15,0,15]) #sensor 4
        sensor5.append(u_k[15,15,15]) #sensor 5
        sensor6.append(u_k[15,29,15]) #sensor 6
        sensor1.append(u_k[15,0,29]) #sensor 1
        sensor2.append(u_k[15,15,29]) #sensor 2
        sensor3.append(u_k[15,29,29]) #sensor 3
        sensor7.append(u_k[29,0,29]) #sensor 7
        sensor8.append(u_k[29,15,29]) #sensor 8
        sensor9.append(u_k[29,29,29]) #sensor 9


    # Se acondicina el for para 3 dimensiones
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

    u_k[:,-1,:] = 20 + 10* sin((2*math.pi/24)*t)
 
    print "Tmax = ", u_k.max()
 
#print "Calores del punto [29,29, 29], en funcion del tiempo (t):"
#print sensor1
#print "Tiempos t:"
#print numeros


# Se imprime el grafico con cada una de las curvas que muestran la variacion de calor en el tiempo
# en cada uno de los sensores (posicion)

pyplot.plot(numeros,sensor1)
pyplot.plot(numeros,sensor2)
pyplot.plot(numeros,sensor3)
pyplot.plot(numeros,sensor4)
pyplot.plot(numeros,sensor5)
pyplot.plot(numeros,sensor6)
pyplot.plot(numeros,sensor7)
pyplot.plot(numeros,sensor8)
pyplot.plot(numeros,sensor9)

# Titulo del grafico y nombre de los ejes
pyplot.title("Variacion de calor v/s Tiempo")
pyplot.xlabel("Tiempo")
pyplot.ylabel("Calor")

# Label de cada una de las curvas
pyplot.plot(sensor1, label = "Sensor 1")
pyplot.plot(sensor2, label = "Sensor 2")
pyplot.plot(sensor3, label = "Sensor 3")
pyplot.plot(sensor4, label = "Sensor 4")
pyplot.plot(sensor5, label = "Sensor 5")
pyplot.plot(sensor6, label = "Sensor 6")
pyplot.plot(sensor7, label = "Sensor 7")
pyplot.plot(sensor8, label = "Sensor 8")
pyplot.plot(sensor9, label = "Sensor 9")

# Ubicacion de las leyendas
pyplot.legend(loc="upper left")

pyplot.show()