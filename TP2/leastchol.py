# ------------------------------------------------------------------------------
#  @file     +leastchol.py+
#  @brief    +Cuadrados mínimos+
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
# Resolución de sistemas de ecuaciones con la descomposición Cholesky
def leastsq(A, b):
    N = len(A)      #Numero de filas
    Nc = len(A[0])  #Numero de columnas

    At = transpuesta(A, N, Nc)
    
    if (autovalores(At@A).min() <= 0 or not esSimetrica(At@A, Nc)):
        print("La matriz no es definida positiva")
        return None

    X = np.zeros(Nc)

    G = Cholesky(At@A, Nc)
    Gt = transpuesta(G, Nc, Nc)

    Y = LsolverLower(G, At@b)
    X = LsolverUpper(Gt, Y)
    return X

# Calculo de la descomposición Cholesky
def Cholesky(A, N):
    G = np.zeros((N,N)) # G es la matriz de Cholesky
    for i in range(N):
        for j in range(i+1):
            suma = 0
            for k in range(j):
                suma += G[i][k]*G[j][k] # suma es la suma de los elementos de la fila anterior
            if (i == j):
                G[i][i] = np.sqrt(A[i][i] - suma) # G[i][i] es el elemento diagonal de la matriz de Cholesky
            else:
                G[i][j] = (A[i][j] - suma)/G[j][j] # G[i][j] es el elemento de la matriz de Cholesky
    return G # Retornamos la matriz de Cholesky

#Resuelve el cálculo de un sistema lineal con una matriz triangular inferior
def LsolverLower(Lm, B):       
    n = len(B)
    Y = np.zeros(n)
    for i in range(n):
        suma = 0
        for j in range(i):
            suma += Lm[i][j]*Y[j]
        Y[i] = (B[i] - suma)/Lm[i][i]
    return Y

#Resuelve el cálculo de un sistema lineal con una matriz triangular superior 
def LsolverUpper(Um, Y):        
    n = len(Y)
    X = np.zeros(n)
    for i in range(n-1,-1,-1):
        suma = 0
        for j in range(n-1,i-1,-1):
            suma += Um[i][j]*X[j]
        X[i] = (Y[i] - suma)/Um[i][i]
    return X

# Calculo de autovalores de la matriz A
def autovalores(A):
    aVa = np.linalg.eigvals(A)
    return aVa

# Calculo de la transpuesta
def transpuesta(mat, N, Nc):
    trans = np.empty((Nc, N))
    for i in range(Nc):
        for j in range(N):
            trans[i][j] = mat[j][i]
    return trans
  
# True si es simetrica, False sino
def esSimetrica(mat, N):
    for i in range(N):
        for j in range(i,N):
            if (mat[i][j] != mat[j][i]):
                return False
    return True


# ------------------------------------------------------------------------------
# TEST    
# ------------------------------------------------------------------------------
def comp(A, b):
    At = transpuesta(A, len(A), len(A[0]))
    print("\n")
    # Método del grupo 4 para resolución de sistemas de ecuaciones
    X = leastsq(A, b)
    print("Resultado calculado: ",X)

    # Método de numpy para resolución de sistemas de ecuaciones
    X1= np.linalg.lstsq(A, b, rcond=None)[0]
    print("Resultado de linalg: ", X1)
    
    if (X is None): # Si no es definida positiva 
        return 1    # No se puede resolver por Cholesky

    if np.allclose(X, X1):      # Comparamos las dos matrices 
        print("Prueba exitosa")
        return 1
    else:
        print("Prueba fallida")
        return 0


def test():
    pOk=0; ptotales=0
    
    A = np.array([[-1,-1],[1,0]])   
    b = np.zeros((2,1)); b=[0,1]
    pOk += comp(A, b)
    ptotales+=1

    A = np.array([[2,-1],[-1,2]])
    b = np.zeros((2,1)); b=[3,8]
    pOk += comp(A, b)
    ptotales+=1

    A = np.array([[0,1],[0,1]])     # Matriz no definida positiva 
    b = np.zeros((2,1)); b=[0,0]
    pOk += comp(A, b)               
    ptotales+=1

    A = np.array([[0,-0.45],[10000,0]])
    b = np.zeros((2,1)); b=[0.003,-87]
    pOk += comp(A, b)
    ptotales+=1

    A = np.array([[2, -1, 0],[-1, 2, -1],[0, -1, 2]])
    b = np.zeros((3,1)); b=[1,2,3]
    pOk += comp(A, b)
    ptotales+=1

    A = np.array([[-8, 1.1, 0],[-1, 3, 1],[0, 7, 5]])
    b = np.zeros((3,1)); b=[15,8,3.2]
    pOk += comp(A, b)
    ptotales+=1

    print(f"Se superaron: {pOk} de {ptotales} pruebas totales")


# ------------------------------------------------------------------------------
# Aplicación práctica de cuadrados mínimos   
# ------------------------------------------------------------------------------
def sonido():
    #Cargamos y mostramos los datos del TP
    df  = pd.read_csv('sound.txt',header=None,names=['ti','yi'],dtype={'ti':np.float64,'yi':np.float64},sep=' ')

    ti  = np.array(df['ti'].tolist())
    yi  = np.array(df['yi'].tolist())


    A = [np.cos(1000*np.pi*ti), np.cos(2000*np.pi*ti), np.cos(3000*np.pi*ti),np.sin(1000*np.pi*ti), np.sin(2000*np.pi*ti), np.sin(3000*np.pi*ti)]
    At = np.transpose(A)
    b = np.asarray(yi)

    Xvect = leastsq(At, b)  # Se carga la transpuesta de A y se resuelve el sistema de ecuaciones

    ycalc= At@Xvect #Calculamos los valores de y a partir de las contantes calculadas

    error = np.subtract(yi, ycalc) #Calculamos el error

    #Graficamos los datos para ver la similitud
    plt.plot(ti,yi, label="Teórica")
    plt.plot(ti, ycalc, label="Aproximada")
    plt.get_current_fig_manager().window.showMaximized()
    plt.tight_layout()
    plt.legend()
    plt.show()

    return Xvect, error