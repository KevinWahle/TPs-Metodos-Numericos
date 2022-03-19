# ------------------------------------------------------------------------------
#  @file     +PuntoFlotante.py+
#  @brief    +Implementación del punto flotante IEEE 754 de 16 bits+
#  @author   +Grupo 4+
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LIBRARIES
# ------------------------------------------------------------------------------
import math

# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------
class binary16:
    def __init__(self, number):
        self.d = 0
        self.bits = [0]*16
        self.dec2bin(number)  # Devuelve si el numero es un caso extremo y cual
        self.bin2dec()

    def dec2bin(self, number):
        ne = 5  # Cantidad de Bits de Exponente
        nm = 10 # Cantidad de Bits de Mantisa
        sesgo = 2**(ne-1)-1 
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
        # Si el número es Normal
        else:
            expTotal = math.floor(math.log2(modulo))    # Calculo el exponente total (e - sesgo)
            exp = expTotal + sesgo                      # Calculo el exponente (e)
            self.bits[1:6]=exp2bin (exp, ne)            # Guardo el exponente en binario
            mantisa = (modulo/2**expTotal) - 1          # Calculo la mantisa

        self.bits[6:16]=man2bin (mantisa, nm)           # Guardo la mantisa en binario

    def bin2dec(self):
        ne = 5  # Cantidad de Bits de Exponente
        nm = 10 # Cantidad de Bits de Mantisa
        sesgo = 2**(ne-1)-1
        
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
def exp2bin (exp, expBits):     # Convierte un numero decimal en binario con potencias positivas
    cont = 0
    expb=[]

    if exp > 2**expBits:        # Numero mayor de lo que puedo guardar
        return [1, 1, 1, 1, 1]
        
    while cont<expBits:
        expb = [exp%2] + expb   # Divido por 2 y me quedo con el resto
        exp = exp // 2 
        cont += 1
    return expb    

def man2bin (man, manBits):     # Convierte un numero decimal en binario con potencias negativas
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

def test():
    # Numero positivo
    operationTest(4.7)
    print("\n")

    # Numero negativo
    operationTest(-3.14)
    print("\n")

    # Numero subnormal
    operationTest(3e-7)
    print("\n")

    # Numero subnormal negativo
    operationTest(-3e-7)
    print("\n")

    # Numero muy cercano a cero -> 0
    operationTest(-5e-10)
    print("\n")

    # Numero mayor al mas grande -> inf
    operationTest(999999999)
    print("\n")

    # Numero menor al mas chico -> -inf
    operationTest(-999999999)
    print("\n")

    # Infinito de float
    operationTest(float('+inf'))
    print("\n")

    # Infinito negativo de float
    operationTest(float('-inf'))
    print("\n")

    # Not a Number de float
    operationTest(float('NaN'))
    print("\n")

# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
test()