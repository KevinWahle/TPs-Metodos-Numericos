# ------------------------------------------------------------------------------
#  @file     +PuntoFlotante.py+
#  @brief    +Implementación del punto flotante IEEE 754 de 16 bits+
#  @author   +Grupo 4+
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LIBRARIES
# ------------------------------------------------------------------------------
import math
import numpy as np
# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------
ne = 5  # Cantidad de Bits de Exponente
nm = 10 # Cantidad de Bits de Mantisa
sesgo = 2**(ne-1)-1 

class binary16:
    def __init__(self, number):
        self.d = 0
        self.bits = [0]*(1+ne+nm)
        self.dec2bin(number)  # Devuelve si el numero es un caso extremo y cual
        self.bin2dec()

    def dec2bin(self, number):
        # ne = 5  # Cantidad de Bits de Exponente
        # nm = 10 # Cantidad de Bits de Mantisa
        # sesgo = 2**(ne-1)-1 
        expTotal = 0 # Es a lo que se eleva el 2  

        # Si no es un caso extremo
        if number != float('inf') and number != float('-inf') and not math.isnan(number):   
            self.bits[0] = 1 if number < 0 else 0   # Guardo el signo
            modulo = abs(number)                    # y tomo su módulo

        # Si el número es NaN
        if math.isnan(number):                      
            self.bits = [0] + [1]*(ne+nm)
            return True

        # Si el número es infinito    
        if number == float('inf') or number == float('-inf') or modulo > (2-2**(-nm))*2**(2**ne-sesgo-2):   
            self.bits[0] = 1 if number < 0 else 0           # Guardo el signo
            self.bits = [self.bits[0]] + [1]*ne + [0]*nm    # Coloco 1s en el exponente y 0s en la mantisa
            return "+inf" if self.bits[0] == 0 else "-inf"

        # Si el número es menor al  número subnormal mas pequeño, lo consideramos 0
        if modulo < 2**(-nm)*2**(1-sesgo): 
            self.bits = [0]*(ne+nm+1)       # Coloco 0s en el exponente y 0s en la mantisa
            return True

        # Si el número es Sub-Normal
        if modulo < 2**(1-sesgo):
            expTotal=1-sesgo                # Calculo el exponente (1 - sesgo)
            self.bits[1:6]=[0]*ne           # Coloco 0s en el exponente
            mantisa=(modulo/2**expTotal)    # Calculo la mantisa
            type="Sub-Normal"

        # Si el número es Normal
        else:
            expTotal = math.floor(math.log2(modulo))    # Calculo el exponente total (e - sesgo)
            exp = expTotal + sesgo                      # Calculo el exponente (e)
            self.bits[1:6]=entero2bin(exp, ne)            # Guardo el exponente en binario
            mantisa = (modulo/2**expTotal) - 1          # Calculo la mantisa
            type="Normal"

        self.bits[6:16]=frac2bin(mantisa, nm)           # Guardo la mantisa en binario
        self.roundIEEE(number, type)                    # Redondeo el número

        
    def roundIEEE(self, number, type):
        auxnum = IEEE2dec(self.bits, type) 
        aux0b = self.bits[0:6]+entero2bin(entero2dec(self.bits[6:16])+1, nm)    # Calculo el número anterior
        aux0 = IEEE2dec(aux0b, type)
        aux1b = self.bits[0:6]+entero2bin(entero2dec(self.bits[6:16])-1, nm)    # Calculo el número siguente
        aux1 = IEEE2dec(aux1b, type)
        err = [abs(aux0-number), abs(auxnum-number), abs(aux1-number)]      # Calculo los errores
        cercano = listMinIndex(err)                                         # Me quedo con el número que menor error tenga
        if cercano == 0:
            self.bits = aux0b
        elif cercano == 2:
            self.bits = aux1b

    def bin2dec(self):
        # ne = 5  # Cantidad de Bits de Exponente
        # nm = 10 # Cantidad de Bits de Mantisa
        # sesgo = 2**(ne-1)-1
        
        # Caso infinito
        if self.bits[1:] == [1]*ne + [0]*nm:        
            self.d= float('inf') if self.bits[0] == 0 else float('-inf')    # Depenendiendo del signo el número sera -inf o +inf
            return True

        # Caso NaN
        elif self.bits[1:6] == [1]*ne:         
            self.d= float('NaN')
            return True

        # Caso 0
        if self.bits[1:] == [0]*ne + [0]*nm:        
            self.d = float(0)

        # Caso Sub-Normal
        elif self.bits[1:6] == [0]*ne:              
            mantis = 0
            for i in range(nm):
                mantis += self.bits[i+6]* 2**(-i-1)             # Calculo la mantisa en decimal         
            self.d = (-1)**self.bits[0]*mantis*2**(1-sesgo)     # Armo mi número en decimal

        # Caso Normal
        else:                                       
            mantis = 1
            for i in range(nm):
                mantis += self.bits[i+6] * 2**(-i-1)            # Calculo la mantisa en decimal
            expo = 0
            for j in range(ne):
                expo += self.bits[j+1] * 2**(ne-j-1)            # Calculo el exponente en decimal
            self.d = (-1)**self.bits[0]*mantis*2**(expo-sesgo)  # Armo mi número decimal  

    # Multiplicación por +1
    def __pos__(self):
        if self.d == float('-inf'):
            return binary16(float('-inf'))
        return binary16(self.d)
        
    # Multiplicación por -1   
    def __neg__(self):
        if self.d == float('inf'):
            return binary16(float('-inf'))
        return binary16(-self.d)
    
    # Suma
    def __add__(self,other):    
        d=self.d+other.d
        return binary16(d)
        
    # Resta
    def __sub__(self,other):
        d=self.d-other.d
        return binary16(d)

    # In-Place Suma
    def __iadd__(self,other):    
        self = binary16(self.d+other.d)
        return self
        
    # In-Place Resta
    def __isub__(self,other):
        self=binary16(self.d-other.d)
        return self

# ------------------------------------------------------------------------------
# FUNCTION DEF
# ------------------------------------------------------------------------------
def entero2bin (exp, expBits):     # Convierte un numero entero base 10 en binario con potencias positivas
    cont = 0
    expb=[]

    if exp > 2**expBits:        # Numero mayor de lo que puedo guardar
        return [1]*expBits      # Coloco 1s en el exponente
        
    while cont<expBits:
        expb = [exp%2] + expb   # Divido por 2 y me quedo con el resto
        exp = exp // 2 
        cont += 1
    return expb    

def entero2dec(bits):           # Convierte un numero entero binario en decimal
    sum=0
    for i in range(len(bits)):
        sum += bits[len(bits)-1-i] * 2**i
    return sum

def frac2bin (man, manBits):     # Convierte un numero decimal en binario con potencias negativas
    cont = 0
    manb=[]
      
    while cont<manBits:         
        man *= 2                # Multiplico al numero por 2, y dependiendo de si es mayor a 1 o no, armo el binario
        if man>=1:
            manb = manb + [1]
            man -= 1
        else:
            manb = manb + [0]      
        cont += 1

    return manb

def frac2dec(bits):             # Convierte un numero racional codificado en binario a decimal
    mant = 0
    for i in range(-len(bits),0):
        mant += bits[-i-1] * 2**i
    return mant

def IEEE2dec(bits, type=""):
        mantis = frac2dec(bits[6:])
        if type == "Sub-Normal":
            return (-1)**bits[0]*mantis*2**(1-sesgo)        # Armo mi número en decimal

        elif type == "Normal":                                       
            expo = entero2dec(bits[1:6])
            return (-1)**bits[0]*(1+mantis)*2**(expo-sesgo)     # Armo mi número decimal
        
        return 0

def listMinIndex(list):      
    min=0                  
    for i in range(len(list)):  # Recorro toda la lista
        if list[i]<list[min]:   # Si el elemento actual es menor al que tengo que comparar
            min=i               # Actualizo el índice del valor del minimo
    return min

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                                TestBench DEF
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def operationTest(numb):
    IeeeNumb = binary16(numb)       # Tomo un número
    IeeeNumb2 = binary16(numb*2)    # Tomo otro número
    res = binary16(0)               # Aquí se almacenará el resultado

    print('Numero inicial:', numb)
    print('Numero guardado:', IeeeNumb.d)

    print("SUMA")
    res = IeeeNumb + IeeeNumb2
    print('a+b: ',IeeeNumb.d, '+', IeeeNumb2.d,'=', res.d, '-> IEEE754: ', res.bits)

    print("RESTA")
    res = IeeeNumb - IeeeNumb2
    print('a-b: ', IeeeNumb.d, '-', IeeeNumb2.d, '=', res.d, '-> IEEE754: ', res.bits)

    print("SUMA2")
    res =  IeeeNumb
    res += IeeeNumb2
    print('a+=b: ',IeeeNumb.d, '+=' , IeeeNumb2.d, '=', res.d,'-> IEEE754: ', res.bits)

    print("RESTA2")
    res =  IeeeNumb
    res -= IeeeNumb2
    print('a-=b: ',IeeeNumb.d, '-=' , IeeeNumb2.d, '=', res.d,'-> IEEE754: ', res.bits)

    print("POS")
    res = +IeeeNumb
    print('+a: ', IeeeNumb.d, '=', res.d, '-> IEEE754: ', res.bits)

    print("NEG")
    res = -IeeeNumb
    print('-a: ', '-', IeeeNumb.d , '=', res.d, '-> IEEE754: ', res.bits)

    return 1 if (IeeeNumb.d==np.float16(numb) and IeeeNumb2.d==np.float16(numb*2)) else 0

def test():
    passCases=0 #Casos que se pasaron
    totalCases=0


    # Numero positivo
    passCases+=operationTest(4.7)
    totalCases+=1
    print("\n")

    # Numero negativo
    passCases+=operationTest(-3.14)
    totalCases+=1
    print("\n")

    # Numero subnormal
    passCases+=operationTest(3e-7)
    totalCases+=1
    print("\n")

    # Numero subnormal negativo
    passCases+=operationTest(-3e-7)
    totalCases+=1
    print("\n")

    # Numero muy cercano a cero -> 0
    passCases+=operationTest(-5e-10)
    totalCases+=1
    print("\n")

    # Numero mayor al mas grande -> inf
    passCases+=operationTest(999999999)
    totalCases+=1
    print("\n")

    # Numero menor al mas chico -> -inf
    passCases+=operationTest(-999999999)
    totalCases+=1
    print("\n")

    # Infinito de float
    passCases+=operationTest(float('+inf'))
    totalCases+=1
    print("\n")

    # Infinito negativo de float
    passCases+=operationTest(float('-inf'))
    totalCases+=1
    print("\n")

    # Not a Number de float
    operationTest(float('NaN'))
    print("\n")

    print ('Las pruebas pasadas con éxito fueron', passCases, '/', totalCases)

# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
test()