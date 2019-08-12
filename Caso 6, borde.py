from matplotlib.pylab import *

L = 1.      # Largo del dominio
n = 100      # Numero de intervalos

dx = L / n   # discretizacion espacial

# Vector con todos los x... puntos del espacio
x = linspace(0,L,n+1)

def recta (x):
	return 10*x

recta = recta(x)
# condicion inicial
def fun_u0(x):
	return 10*exp(-(x-0.5)**2/0.1**2)

u0 = fun_u0(x)

#creando el vetor de solucion u en el tiempo o paso k
u_k = u0.copy() #copy crea una nueva instancia del vector en memoria

#Condiciones de borde (esenciales)
u_k[0] = 0
u_k[n] = 10

#temperatura en el tiempo K +1 = dt * (k+1)
u_km1 = u_k.copy()

#Parametros del problema (hierro)
dt = 1.       # s
K = 79.9	  # m**2 / s
c = 450.	  # J / kg C
rho = 7800.    # kg / m**3
alpha = K*dt/(c*rho*dx**2)

print "dt =" , dt
print "dx =" , dx	
print "k ="  , K
print "c ="  , c
print "rho =" , rho
print "alpha =" ,alpha

plot(x,u0,"k--")


# loop en el tiempo

k = 0
for k in range (70000):
	t= dt*k
	print "k =", k, "t =", t
	u_k[0] = 0.
	u_k[n] = 10.
	#loop en el espacio i = ... n-1   u_km[0] = 0, u_km[n] =20
	for i in range(1,n):
		#print i
		#Algoritmo de diferencias finitas 1-D para difusion
		if u_k[i] < recta[i]:
			u_km1[i] = recta [i]
		else:	 
			u_km1[i] = u_k[i] + alpha*(u_k[i+1] - 2*u_k[i] + u_k[i-1])
	#Avanzar la solucion a k +1
	u_k = u_km1

	if k % 1000 == 0:
		plot(x,u_k)
		
title("k ={}   t={} s".format(k, k*dt))

show()
