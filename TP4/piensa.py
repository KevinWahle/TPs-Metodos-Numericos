# ------------------------------------------------------------------------------
#  @file     +piensa.py+
#  @brief    +Ecuaciones diferenciales ordinarias+
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
# Resolución de ecuaciones diferenciales con RK4
def ruku4(f, t0, tf, h, x0):
    n = int ((tf-t0)/h) # Número de elementos del vector
    t=np.linspace(t0, tf, n+1) # Vector de tiempos 
    x=np.zeros((n+1, len(x0))) # Matriz x: tiene una fila por cada instante de tiempo y una columna dada por el tamaño de x0
    x[0]=x0
    # Resolución de la ecuación diferencial con Runge-Kutta de orden 4
    for i in range(n):
        f1=f(t[i],x[i])
        f2=f(t[i]+h/2,x[i]+(h/2)*f1)
        f3=f(t[i]+h/2,x[i]+(h/2)*f2)
        f4=f(t[i]+h,x[i]+h*f3)
        x[i+1]=x[i]+h*(f1+2*f2+2*f3+f4)/6
    return t, x

def ModeloHH(t,x):
    # Parámetros de la ecuación diferencial
    g_Na=120; g_K=36 ; g_L=0.3
    E_Na=115; E_K=-12; E_L=10.6
    C_m=1
    V_Na=50;  V_K=-77; V_L=-54.4
    ic = 8.875

    v=x[0]; n=x[1]; m=x[2]; h=x[3]

    alfa_n = lambda v: 0.01*((v+55)/(1-np.exp(-(v+55)/10)))
    alfa_m = lambda v: 0.1*((v+40)/(1-np.exp(-(v+40)/10)))
    alfa_h = lambda v: 0.07*np.exp(-(v+65)/20)
    beta_n = lambda v: 0.125*np.exp(-(v+65)/80)
    beta_m = lambda v: 4*np.exp(-(v+65)/18)
    beta_h = lambda v: 1/(1+np.exp(-(v+35)/10))

    # Ecuaciónes diferenciales
    fv = ic-g_Na*(m**3)*h*(v-V_Na)-g_K*(n**4)*(v-V_K)-g_L*(v-V_L)
    fn = alfa_n(v)*(1-n)-beta_n(v)*n
    fm = alfa_m(v)*(1-m)-beta_m(v)*m
    fh = alfa_h(v)*(1-h)-beta_h(v)*h      

    return np.array([fv,fn,fm,fh])

def hodgkinhuxley():
    #Definimos las condiciones iniciales
    x0=np.array([-65,0,0,0])
    t0=0
    tf=200
    h=0.01
    t,x=ruku4(ModeloHH,t0,tf,h,x0)

    #Graficamos las soluciones
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(t0-5.0, tf)
    ax.set_ylim(-80, 50)
    plt.plot(t,x[:,0])
    plt.title("Modelo de Hodgkin-Huxley")
    plt.xlabel("t (ms)")
    plt.ylabel("v(t) (mV)")
    plt.grid()
    plt.show()

    return t,x

def test():
    x0=np.array([0])
    t0=0; tf=10; h=0.01

    testfun=np.zeros(1)
    f = lambda t: t**2
    sol = lambda t: t**3
    testfun=np.append(testfun, [f, f])

    f = lambda t: np.sin(t)
    sol = lambda t: np.cos(t)
    testfun=np.append(testfun, [f, f])

    f = lambda t: mt.log(t, np.e)
    sol = lambda t: 1/t
    testfun=np.append(testfun, [f, f])

    f = lambda t: np.e**t
    testfun=np.append(testfun, [f, f]) # La integral de la exponencial es ella misma
    
    for func, sol in testfun:
        t_rk, x_rk = ruku4(f=func, t0=t0, tf=tf, x0=x0)
        plt.plot(t_rk, x_rk, label="RK-4")
        x = sol(t_rk)
        plt.plot(t,x, label="solución")
        plt.legend()
        plt.show()

test()