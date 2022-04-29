# ------------------------------------------------------------------------------
#  @file     +mri.py+
#  @brief    +Ecuaciones no-lineales+
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
# Resolución de ecuaciones no-lineales
def solver(L,l,n):
    tol = 1e-9
    maxiter = 100

    mu = 4 * np.pi * 10**(-7)   # Permeabilidad del vacío
    ro = 0.1                    # Radio del solenoide en metros
    
    # Función a resolver
    f = lambda r:(((mu * n**2 * np.pi * r**2) / (l**2)) * (np.sqrt(r**2 + l**2) - r))-L
    # Derivada de la función a resolver
    df = lambda r: (n**2*np.pi*r*(-r + np.sqrt(l**2 + r**2))*(-r + 2*np.sqrt(l**2 + r**2))*mu)/(l**2 * np.sqrt(l**2 + r**2))
    
    #--------------- NEWTON-RAPHSON -------------------------------------------     
    for iters in range(maxiter): # Iteramos como máximo maxiter veces
        dr = f(ro)/df(ro)
        ro = ro-dr
        if abs(dr) < tol:   # Si se llega a un error menor al deseado, terminamos
            break
    
    return ro, iters


def graphRvL():
    C = 10000                       # Cantidad de puntos a tomar
    l = 0.2                         # Longitud del solenoide en metros
    L = np.linspace(1e-9,100e-6,C)  # Inductancia del solenoide H
    N = [10, 100, 1000]             # Cant de vueltas

    #Inicialización de arreglos
    r1 = np.zeros(C); r2 = np.zeros(C); r3 = np.zeros(C)    

    for i in range(C):  # Calculo de radios para cada numero de espiras
        r1[i],_ = solver(L[i],l,N[0])
        r2[i],_ = solver(L[i],l,N[1])
        r3[i],_ = solver(L[i],l,N[2])

    # Graficación
    fig, axs = plt.subplots(3, sharex=True)
    fig.suptitle('Radio vs Inductancia')
    axs[0].plot(L*1e6, r1*1000, color="r")
    axs[1].plot(L*1e6, r2*1000, color="b")
    axs[2].plot(L*1e6, r3*1000, color="k")
    
    # Configuraciones de los ejes
    axs[0].set_title('N = 10'); axs[0].grid('both')
    axs[1].set_title('N = 100') ; axs[1].grid('both')
    axs[2].set_title('N = 1000') ; axs[2].grid('both')
    fig.supxlabel('Inductancia [uH]')
    fig.supylabel('Radio [mm]')
    
    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()


def test():
    tol = 1e-9              # Tolerancia aceptada
    mu = 4 * np.pi * 10**(-7)   # Permeabilidad del vacío
    l = np.linspace(0.02,1,100) # Longitudes del solenoide en metros
    L = np.linspace(1e-9,100e-6,100) # Inductancias del solenoide H
    n = np.linspace(1,100,100)  # Cantidad de espiras

    # Calculo de la inductancia
    Lcalc = lambda r,l,n:((mu * n**2 * np.pi * r**2) / (l**2)) * (np.sqrt(r**2 + l**2) - r)

    result=0 ; tot=0

    for l_ in l:
        for L_ in L:
            for n_ in n:
                tot+=1

                # Calculo del radio para cada valor de cada parámetro
                r,_ = solver(L_,l_,n_) 

                # Verificación del radio obtenido
                result = result + 1 if abs(L_ - Lcalc(r,l_,n_)) < tol else result   
    
    print('Se pasaron con éxito', result, '/', tot, 'casos')