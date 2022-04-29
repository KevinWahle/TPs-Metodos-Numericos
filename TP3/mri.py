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

    mu = 4 * np.pi * 10**(-7) # Permeabilidad del vacío
    ro = 0.1 # Radio del solenoide en metros
    f = lambda r:(((mu * n**2 * np.pi * r**2) / (l**2)) * (np.sqrt(r**2 + l**2) - r))-L
    df = lambda r: (n**2*np.pi*r*(-r + np.sqrt(l**2 + r**2))*(-r + 2*np.sqrt(l**2 + r**2))*mu)/(l**2 * np.sqrt(l**2 + r**2))
    
    #--------------- NEWTON-RAPHSON -------------------------------------------     
    for iters in range(maxiter):
        dr = f(ro)/df(ro)
        ro = ro-dr
        if abs(dr) < tol:
            break
    
    return ro, iters

def graphRvL():
    C = 10000
    l = 0.2 # Longitud del solenoide en metros
    L = np.linspace(1e-9,100e-6,C) # Inductancia del solenoide H
    N = [10, 100, 1000]
    r1 = np.zeros(C); r2 = np.zeros(C); r3 = np.zeros(C)

    for i in range(C):
        r1[i],_ = solver(L[i],l,N[0])
        r2[i],_ = solver(L[i],l,N[1])
        r3[i],_ = solver(L[i],l,N[2])

    fig, axs = plt.subplots(3, sharex=True)
    fig.suptitle('Radio vs Inductancia')
    axs[0].plot(L*1e6, r1*1000, color="r")
    axs[1].plot(L*1e6, r2*1000, color="b")
    axs[2].plot(L*1e6, r3*1000, color="k")
    
    # Names
    axs[0].set_title('N = 10'); axs[0].grid('both')
    axs[1].set_title('N = 100') ; axs[1].grid('both')
    axs[2].set_title('N = 1000') ; axs[2].grid('both')
    fig.supxlabel('Inductancia [$\mu H$]')
    fig.supylabel('Radio [mm]')
    
    plt.tight_layout()

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

def test():
    C = 100
    Cl = 100
    Cn = 100
    l = np.linspace(0.02,1,C) # Longitud del solenoide en metros
    L = np.linspace(1e-9,100e-6,Cl) # Inductancia del solenoide H
    n = np.linspace(1,100,Cn)
    mu = 4 * np.pi * 10**(-7) # Permeabilidad del vacío
    Lcalc = lambda r:((mu * n**2 * np.pi * r**2) / (l**2)) * (np.sqrt(r**2 + l**2) - r)
    
    tol = 1e-9
    for l_ in l:
        for L_ in L:
            for n_ in n:
                r,_ = solver(L_,l_,n_)
                print(L_, r)
                if abs(L_ - Lcalc(r)) < tol:
                    result = result + 1

    # tol = 1e-9
    # result = 0
    # r = np.zeros(C*Cl*Cn)
    # for i in range(C):
    #     for ii in range(Cl):
    #         for iii in range(Cn):
    #             r[i][ii][iii],_ = solver(L[i],l[ii],n[iii])
    #             if abs(L[i]-Lcalc(r[i][ii][iii])) < tol:
    #                 result = result + 1

    # r = np.zeros(C*Cl*Cn)
    # for i in range(C):
    #     for ii in range(Cl):
    #         for iii in range(Cn):
    #             r[i+ii+iii],_ = solver(L[i],l[ii],n[iii])
    
    # tol = 1e-9
    # result = 0
    # for j in range(C):
    #     if abs(L[j]-Lcalc(r[j])) < tol:
    #         result = result + 1

    print('Se pasaron con éxito', result, '/', C*Cl*Cn, 'casos')

test()
#graphRvL()