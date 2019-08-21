from matplotlib.pylab import *
 
 
a = 1.          #Ancho del dominio
b = 1.          #Largo del dominio
Nx = 30         #Numero de intervalos en x
Ny = 30         #Numero de intervalos en Y
 
dx = b / Nx     #Discretizacion espacial en X
dy = a / Ny     #Discretizacion espacial en Y
 
h = dx    # = dy
 
 
if dx != dy:
    print("ERRROR!!!!! dx != dy")
    exit(-1)   #-1 le dice al SO que el programa fallo.....
 
#Funcion de conveniencia para calcular coordenadas del punto (i,j)
 
# def coords(i,j):
#   return dx*i, dy*j
# x, y = coords(4,2)  
 
# i, j = 4, 2 
# x, y = dx*i, dy*j
 
coords = lambda i, j : (dx*i, dy*j)
x, y = coords(4,2) 
 
print "x = ", x
print "y = ", y
 
# Dado que la condicion inicial es que la temeperatura intera es de 20 grados celsius
# se crea una matriz con puros numeros 20 en su interior


u_k = 20*ones((Nx+1,Ny+1), dtype=double)   #dtype es el tipo de datos (double, float, int32, int16...)
u_km1 = 20*ones((Nx+1,Ny+1), dtype=double)   #dtype es el tipo de datos (double, float, int32, int16...)
 
#CB esencial
# Se aplica las condiciones base del problema
u_k[0,:] = 20.
u_k[-1,:] = 20.

 
#Buena idea definir funciones que hagan el codigo expresivo
def printbien(u):
    print u.T[Nx::-1,:]
 
print u_k               #Imprime con el eje y invertido
printbien(u_k)
 
def imshowbien(u):
    imshow(u.T[Nx::-1,:])
    colorbar(extend='both',cmap='plasma')
    clim(10, 30)   # Segun el video la barra de temperatura va de 10 a 30 grados celsius
 
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
# Se fija un valor de 60 de tal forma de que arroje mas imagenes
for k in range(int32(60./dt)):
    t = dt*(k+1)
    print "k = ", k, " t = ", t
 
    #CB esencial
    # Se fijan las condiciones basales
    u_k[0,:] = 20.
    u_k[-1,:] = 20.

    # Se fija la funcion de variacion de calor en la cara superior 
    u_k[:,-1] = 20 + 10* sin((2* math.pi/24)*t )
 
    #Loop en el espacio   i = 1 ... n-1   u_km1[0] = 0  u_km1[n] = 20
    for i in range(1,Nx):
        for j in range(1,Ny):
            #Algoritmo de diferencias finitas 2-D para difusion
 
            #Laplaciano
            nabla_u_k = (u_k[i-1,j] + u_k[i+1,j] + u_k[i,j-1] + u_k[i,j+1] - 4*u_k[i,j])/h**2
 
            #Forward euler..
            u_km1[i,j] = u_k[i,j] + alpha*nabla_u_k
 
    #CB natural
    u_km1[Nx,:] = u_km1[Nx-1,:]
    u_km1[:,Ny] = u_km1[:,Ny-1]
 
    #Avanzar la solucion a k + 1
    u_k = u_km1
 
    #CB esencial una ultima vez
    # Nuevamente se fijas las condiciones bases y ademas se fija la funcion de variacion
    # de calor de la cara superior
    u_k[0,:] = 20.
    u_k[-1,:] = 20.
    u_k[:,-1] = 20 + 10* sin((2*math.pi/24)*t)
 
    print "Tmax = ", u_k.max()
 
    if t > next_t:
        figure(1)
        imshowbien(u_k)
        title("k = {0:4.0f} t   t = {1:05.2f} m".format(k, k*dt))
        # Se guarda en la carpeta movie_modificacion
        savefig("movie_modificacion_1/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        close(1)
 
# figure(2)
# imshowbien(u_k)
# title("k = {}   t = {} s".format(k, (k+1)*dt))
 
 
show()