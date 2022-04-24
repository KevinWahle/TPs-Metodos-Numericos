# ------------------------------------------------------------------------------
#  @file     +mri.py+
#  @brief    +Ecuaciones no-lineales+
#  @author   +Grupo 4+
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LIBRARIES
# ------------------------------------------------------------------------------
from termios import NL1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as mt

# ------------------------------------------------------------------------------
# FUNCTION DEF
# ------------------------------------------------------------------------------
# Resolución de ecuaciones no-lineales
def solver(L,l,n):
    mu = 4 * np.pi * 10**(-7) # Permeabilidad del vacío
    r = 1 # Radio del solenoide en metros
    L = ((mu * n**2 * np.pi * r**2) / (l**2)) * (np.sqrt(r**2 + l**2) - r)
    #Hacer la función que resuelva la ecuación!

    return r

def graphRL():
    l = 0.2 # Longitud del solenoide en metros
    L = np.linspace(1e-9,100e-9,1000) # Inductancia del solenoide H
    N1 = 10
    N2 = 100
    N3 = 1000

    r1 = solver(L,l,N1)
    r2 = solver(L,l,N2)
    r3 = solver(L,l,N3)

    plt.plot(L,r1, label = 'N = 10')
    plt.plot(L,r2, label = 'N = 100')
    plt.plot(L,r3, label = 'N = 1000')
    plt.xlabel('Inductancia [H]')
    plt.ylabel('Radio [m]')
    plt.title('Radio vs Inductancia')
    plt.legend()
    plt.show()
