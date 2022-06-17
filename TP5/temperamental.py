# ------------------------------------------------------------------------------
#  @file     +temperamental.py+
#  @brief    +Optimización+
#  @author   +Grupo 4+
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LIBRARIES
# ------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as mt

# ------------------------------------------------------------------------------
# FUNCTION DEF
# ------------------------------------------------------------------------------

data = np.loadtxt("temp.txt") 

# Optimización basada el método de gradientes conjugados usando interpolación cuadrática
def minimi(f, Df, x0, tol, maxiter):
    x = x0
    g = -Df(x) # Gradiente

    # Evaluo primero si el gradiente es menor a la tolerancia
    if(np.linalg.norm(g)<tol):
        print("X0 es un mínimo")
        return x
    
    # Determinamos un alfa para cada paso de interación usando interpolación cuadrática
    for i in range(maxiter):
        alfa = 1
        H = alfa * g 

        a = 0
        fa= f(x+a*H)
        b = 1
        fb= f(x+b*H)
        c = 1/2
        fc= f(x+c*H)
	    #(a,fa) - (c,fc) - (b,fb)	

        while 1 :
            if fa > fc:
                #sigue "bajando"
                if fc > fb:
                    c, fc  = b, fb
                    b *= 2
                    fb = f(x+b*H)
                else:
                    break
            else: 
                #está aumentando
                b, fb  = c, fc
                c  /= 2
                fc = f(x+c*H)
            
            #si el intervalo es demasiado chico o demasiado grande, comencemos nuevamente...
            if (b < 1e-6) or (b > 1e6) :
                alfa = alfa + 1
                if alfa == 50 :
                    break
                b = np.rand
                c /= 2
        # Si después de muchas iteraciones, no llegamos a nada, devuelvo algo al azar entre 0 y 1.
        if alfa == 50 :
            print("No se encontró una solución")
            alfa = np.rand(0,1)
        else:
            alfa_min = c*((4*fc-fb-3*fa)/(4*fc-2*fb-2*fa))

        x_n = x + alfa_min*H
        x = x_n

    return x


def aux(x):
    return data[:,1]- (x[0]+x[1]*np.cos(2*np.pi*data[:,0]/x[3])+x[2]*np.cos(2*np.pi*data[:,0]/x[4]))

def f(x):
    return np.sum(np.square(aux(x)))

def df(x):
    df=np.zeros(len(x))
    aux = aux(x) 
    df[0]=-2*np.sum(aux)
    df[1]=-2*np.sum(aux*np.cos(2*np.pi*data[:,0]/x[3]))
    df[2]=-2*np.sum(aux*np.cos(2*np.pi*data[:,0]/x[4]))
    df[3]=-2*np.sum(aux*x[1]*np.pi*2*data[:,0]*np.sin(2*np.pi*data[:,0]/x[3])/(x[3]**2)) 
    df[4]=-2*np.sum(aux*x[2]*np.pi*2*data[:,0]*np.sin(2*np.pi*data[:,0]/x[4])/(x[4]**2))
    return df

def temperatura():
    x0=np.array([36.16230263,0.24203703,0.17812332,23.99802585,23.98588076]) #??
    tol=1e-15
    max_it=10000
    x=minimi(f, g, x0, tol, max_it)
    #Error
    error=abs(aux(x))
    return x, error    

# ------------------------------------------------------------------------------
# TEST
# ------------------------------------------------------------------------------
def test():
    tol=1e-15
    max_it=1000
    #Evaluamos la función minimi
    print("Funciones de prueba para minimi:\n")
    print("\nFunción esférica de orden 3: \n")
    x01=np.array([500,127,4005])
    x1=minimi(f_test_1, g_test_1, x01, tol, max_it)
    x1_r=np.zeros(3)
    print("El mínimo real es: ", x1_r, "mientras que el mínimo calculado por minimi con x0=", x01, "es: ", x1)
    print("La norma de la diferencia entre el mínimo real y el cálculado es:", np.linalg.norm(x1_r-x1))
    #Evaluamos la función temperatura
    print("\n\nEvaluación de la función temperatura: \n")
    x,error=temperatura()
    print("Para los valores de x0 propuestos, se obtienen los siguientes parámetros que minimizan la función:\n")
    print("a=", x[0], "\n")
    print("b=", x[1], "\n")
    print("c=", x[2], "\n")
    print("T1=", x[3], "\n")
    print("T2=", x[4], "\n")
    print("El error promedio obtenido es: ", np.sum(error)/len(error), "ºC\n")
    print("Se obtuvo un error máximo de ", np.max(error),"ºC y un error mínimo de ", np.min(error), "ºC \n")
    print("El error promedio relativo obtenido es: ",
    (np.sum(abs(aux(x)/data[:,1]))/len(error))*100, "% \n")
    return