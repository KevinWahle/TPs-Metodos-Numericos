# ------------------------------------------------------------------------------
#  @file     +temperamental.py+
#  @brief    +Optimización+
#  @author   +Grupo 4+
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LIBRARIES
# ------------------------------------------------------------------------------
from tkinter import Y
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as mt
#import sklearn.metrics as skl
# ------------------------------------------------------------------------------
# FUNCTION DEF
# ------------------------------------------------------------------------------
data = np.loadtxt("temp.txt") 
t=data[:,0]; y=data[:,1]

#Optimización basada el método de gradientes conjugados usando interpolación cuadrática
def minimi(f, Df, x0, tol, maxiter):
    x = x0
    g = -Df(x) # Gradiente

    # Evaluo primero si el gradiente es menor a la tolerancia
    if(np.linalg.norm(g)==0):
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
                if alfa == 100 :
                    break
                b = np.random.rand(1)
                c /= 2
        
        # Si después de muchas iteraciones, no llegamos a nada, devuelvo algo al azar entre 0 y 1.
        if alfa == 100 :
            alfa_min = np.random.rand(1)
        else:
            alfa_min = c*((4*fc-fb-3*fa)/(4*fc-2*fb-2*fa))
        
        x_n = x + alfa_min*H
        if(np.linalg.norm(x_n-x)<tol):
            print("Se encontró~ una solución")
            break
        x = x_n
    return x

# def minimi(funcion, gradiente, x0, tol, max_it): 
#     x=x0 
#     d=-gradiente(x) 
#     if(np.linalg.norm(d)==0): 
#         print("x0 es min") 
#         return x 
#         #Determinamos alfa_min para cada paso de iteracion usando interpolacion cuadratica
#     for i in range(max_it):
#     #Definimos un alfa_0 experimentalmente
#         alfa=1
#         h=alfa*d
#         f_a=funcion(x)
#         f_b=funcion(x+h)
#         f_c=funcion(x+2*h)
#         for j in range(1000):
#             if((f_b<f_a) and (f_b<f_c)):
#                 break
#             elif((f_a>f_b) and (f_b>f_c)):
#                 alfa=2*alfa
#                 f_b=f_c
#                 f_c=funcion(x+alfa*2*d)
#             elif((f_a<f_b) and (f_b<f_c)):
#                 alfa=alfa/2
#                 f_c=f_b
#                 f_b=funcion(x+alfa*d)
#             elif(f_a==f_b):
#                 alfa=alfa/2
#                 f_c=f_b
#                 f_b=funcion(x+alfa*d)
#                 break
#             elif(f_b==f_c):
#                 alfa=3*alfa/2
#                 f_a=f_b
#                 f_b=funcion(x+alfa*d)
#                 break
#         if (f_a==f_c):
#             alfa_min=alfa
#         elif(((f_a<f_b) or (f_b>f_c)) and j==999):
#             break
#         else:
#             alfa_min=alfa*(4*f_b-3*f_a-f_c)/(4*f_b-2*f_a-2*f_c)
#         x_n=x+alfa_min*d
#         if(np.linalg.norm(x_n-x)<tol):
#             break
#         x=x_n
#     return x

f_aux= lambda x: y - (x[0]+x[1]*np.cos(2*np.pi*t/x[3])+x[2]*np.cos(2*np.pi*t/x[4]))
f = lambda x: np.sum(np.square(f_aux(x)))/len(f_aux(x))

def grad(coef):
    # coef = [a, b, c, T1, T2]
    df=np.zeros(len(coef))
    difflocal = f_aux(coef)

    df[0]=-2*np.sum(difflocal)  #d/da
    df[1]=-2*np.sum(difflocal*np.cos(2*np.pi*t/coef[3]))   #d/db 
    df[2]=-2*np.sum(difflocal*np.cos(2*np.pi*t/coef[4]))   #d/dc
    df[3]=-2*np.sum(difflocal*coef[1]*np.pi*2*t*np.sin(2*np.pi*t/coef[3])/(coef[3]**2)) #d/dT1
    df[4]=-2*np.sum(difflocal*coef[2]*np.pi*2*t*np.sin(2*np.pi*t/coef[4])/(coef[4]**2)) #d/dT2
    return df

def temperatura():
    xo=np.array([36.16,0.1,1.0,24.00,24.00])
    tol=1e-16; max_it=10000
    x = minimi(f, grad, xo, tol, max_it)
    error = f_aux(x) # Error local
    return x, error    

# ------------------------------------------------------------------------------
# TEST
# ------------------------------------------------------------------------------
def test():
    #tol=1e-15; max_it=1000 ESTAN AL PEDO
    
    #Evaluamos la función temperatura
    x, error=temperatura()
    print("Coef obtenidos ([a,b,c,T1,T2]): \n", x)
    print("ECM: ", np.sum(np.power(error,2))/len(error))
    print("Error Maximo", np.max(np.abs(error)), "ºC")
    print("Error Relativo medio: ", (np.sum(abs(error/y))/len(error))*100, "%")

    temp = lambda t: (x[0]+x[1]*np.cos(2*np.pi*t/x[3])+x[2]*np.cos(2*np.pi*t/x[4]))

    plt.plot(t, y, 'b', label='Datos')
    plt.plot(t, temp(t), 'r', label='Modelo')
    plt.xlim(0, 250)
    plt.legend()
    plt.show()
    return 0

test()