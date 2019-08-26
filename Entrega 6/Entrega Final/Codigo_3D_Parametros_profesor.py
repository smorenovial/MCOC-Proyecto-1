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
 

 
coords = lambda i, j : (dx*i, dy*j,dz*l)
 
# Dado que la condicion inicial es que la temeperatura intera es de 20 grados celsius
# se crea una matriz con puros numeros 20 en su interior


u_k = 20*ones((Nx+1,Ny+1,Nz+1), dtype=double)#dtype es el tipo de datos (double, float, int32, int16...)
u_km1 = 20*ones((Nx+1,Ny+1,Nz+1), dtype=double)  #dtype es el tipo de datos (double, float, int32, int16...)
 
#Parametros del problema (hormigon)

dt = 1.       # hr
K = 9.5       # m^2 / s   
c = 950.       # J / kg C
rho = 2350.    # kg / m^3
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

#Loop en el tiempo 
# Se fija un dnext_t igual a 1 para que vaya avanzando cada un minuto
dnext_t = 1   #  20.00
next_t = 0.
framenum = 0

# Lo relacionado con temperatura
temperatura=[]
# se llama al bloc con las temperaturas:
with open('blocTemperaturaAmbiente.txt','r') as f:
# se crea un array con las temperaturas:
    f_contents = f.read(0)
    for line in f:
        temperatura.append(float(line))
    temperatura = np.array(temperatura)
    


# Se crean las listas que contendran la temperatura de cada sensor en un punto en especifico, en cada tiempo
sensor1=[20]
sensor2=[20]
sensor3=[20]
sensor4=[20]
sensor5=[20]
sensor6=[20]
sensor7=[20]
sensor8=[20]
sensor9=[20]

# lista para guardar cada uno de los valores de Q dependiendo del tiempo 
valoresQ = []
# lista numeros para poder graficar, este es el eje x
numeros = [0]
# tanto po y beta son contadores para que no exista error dentro de las listas sensor(n)
po = 0
beta = 0 # para que solo el primer valor de los sensores sea con valoresQ[0]

# codigo para llamar al excel

# Ciclo que va guardando en la lista valoresQ el calor generado en cada tiempo por el fraguado del hormigon
cantidadk=0

for k in range(int32(40./dt)):

    t = dt*(k+1)
    print "k = ", k, " t = ", t
    Qm= Hu * 220 * ((15.0/t)**0.781429) * (0.781429/t) * 0.75 * exp(-(15.0/t)**0.781429) * exp(27.8284/8.314472*(1/(273+79)-1/(273+21)))
    Qmodificado= Qm*(10**-6)

    valoresQ.append(Qmodificado)


    # Se fija la funcion de variacion de calor en la cara superior 
    u_k[:,-1,:] = temperatura[k]

    cantidadk+=1

    if k % 1 == 0: # Tiempo aproximado valor 1
        if  beta == 0:
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
            beta += 1
            numeros.append(po+1)
        else:
    # Se le suma a la matriz u_k la diferencia de calor generado entre un tiempo y otro
            matrizq= valoresQ[po]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
            matrizq1= valoresQ[po+1]*ones((Nx+1,Ny+1,Nz+1), dtype=double)
            diferencia=matrizq1-matrizq
          
            if (u_k[15,0,15] and u_k[15,15,15] and u_k[15,29,15] and u_k[15,0,29] and u_k[15,15,29] and u_k[15,29,29] and u_k[29,0,29] and u_k[29,15,29] and u_k[29,29,29]) >= 20:
                u_k=u_k+diferencia
                sensor4.append(u_k[15,0,15]) #sensor 4
                sensor5.append(u_k[15,15,15]) #sensor 5
                sensor6.append(u_k[15,29,15]) #sensor 6
                sensor1.append(u_k[15,0,29]) #sensor 1
                sensor2.append(u_k[15,15,29]) #sensor 2
                sensor3.append(u_k[15,29,29]) #sensor 3
                sensor7.append(u_k[29,0,29]) #sensor 7
                sensor8.append(u_k[29,15,29]) #sensor 8
                sensor9.append(u_k[29,29,29]) #sensor 9
                po += 1
                numeros.append(po+1)


            else:
                u_k=u_k+zeros((Nx+1,Ny+1,Nz+1), dtype=double)

        



    # Se acondicina el for para 3 dimensiones
    #Loop en el espacio   i = 1 ... n-1   u_km1[0] = 0  u_km1[n] = 20
    for i in range(1,Nx):
        for j in range(1,Ny):
            for l in range(1,Nz):

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
 
    # Nuevamente se fijas las condiciones bases y ademas se fija la funcion de variacion
    # de calor de la cara superior

    u_k[:,-1,:] = temperatura[k]
 
    print "Tmax = ", u_k.max()
 
# Se imprime el grafico con cada una de las curvas que muestran la variacion de calor en el tiempo
# en cada uno de los sensores (posicion)
# print len(numeros),len(sensor1),len(sensor2),len(sensor3),len(sensor4),len(sensor5),len(sensor6),len(sensor7),len(sensor8),len(sensor9)
# print numeros, "\n"
# print sensor1, "\n"
# print sensor7




temperatura_2=[]



indice=0
for i in temperatura:
    if indice<=cantidadk:
        temperatura_2.append(i)
    indice+=1




# Titulo del grafico y nombre de los ejes
pyplot.title("Variacion de calor v/s Tiempo")
pyplot.xlabel("Tiempo")
pyplot.ylabel("Calor")

# Label de cada una de las curvas






numeros_s1= list(range(1,len(sensor1)+1))
numeros_s2= list(range(1,len(sensor2)+1))
numeros_s3= list(range(1,len(sensor3)+1))
numeros_s4= list(range(1,len(sensor4)+1))
numeros_s5= list(range(1,len(sensor5)+1))
numeros_s6= list(range(1,len(sensor6)+1))
numeros_s7= list(range(1,len(sensor7)+1))
numeros_s8= list(range(1,len(sensor8)+1))
numeros_s9= list(range(1,len(sensor9)+1))


cont_s1=0
for i in sensor1:
    if i<20:
        sensor1[cont_s1]=20
    cont_s1+=1
cont_s2=0
for i in sensor2:
    if i<20:
        sensor2[cont_s2]=20
    cont_s2+=1

cont_s3=0
for i in sensor3:
    if i<20:
        sensor3[cont_s3]=20
    cont_s1+=1
cont_s4=0
for i in sensor4:
    if i<20:
        sensor4[cont_s4]=20
    cont_s4+=1
cont_s5=0
for i in sensor5:
    if i<20:
        sensor5[cont_s5]=20
    cont_s5+=1
cont_s6=0
for i in sensor6:
    if i<20:
        sensor6[cont_s6]=20
    cont_s6+=1
cont_s7=0
for i in sensor7:
    if i<20:
        sensor7[cont_s7]=20
    cont_s7+=1
cont_s8=0
for i in sensor8:
    if i<20:
        sensor8[cont_s8]=20
    cont_s8+=1
cont_s9=0
for i in sensor9:
    if i<20:
        sensor9[cont_s9]=20
    cont_s9+=1


pyplot.plot(numeros_s1,sensor1, label = "Sensor 1")
pyplot.plot(numeros_s2,sensor2, label = "Sensor 2")
pyplot.plot(numeros_s3,sensor3, label = "Sensor 3")
pyplot.plot(numeros_s4,sensor4, label = "Sensor 4")
pyplot.plot(numeros_s5,sensor5, label = "Sensor 5")
pyplot.plot(numeros_s6,sensor6, label = "Sensor 6")
pyplot.plot(numeros_s7,sensor7, label = "Sensor 7")
pyplot.plot(numeros_s8,sensor8, label = "Sensor 8")
pyplot.plot(numeros_s9,sensor9, label = "Sensor 9")
#pyplot.plot(numeros,temperatura_2, label = "Temperatura Ambiente")


# Ubicacion de las leyendas
pyplot.legend(loc="upper left")

pyplot.show()