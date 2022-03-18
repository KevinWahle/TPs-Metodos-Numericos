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
        self.extremo = self.dec2bin(number)  # Devuelve si el numero es un caso extremo y cual
        self.bin2dec()

        # FOR DEBUG
        # print("Signo:", self.bits[0])
        # print("Exp:", self.bits[1:6])
        # print("Mantisa:", self.bits[6:16])

    def dec2bin(self, number):
        ne = 5  # Cantidad de Bits de Exponente
        nm = 10 # Cantidad de Bits de Mantisa
        sesgo = 2**(ne-1)-1 
        expTotal = 0   

        if number != float('inf') and number != float('-inf') and not math.isnan(number):   # Si no es un caso extremo
            self.bits[0] = 1 if number < 0 else 0   # Guardo el signo
            modulo = abs(number)                    # y tomo su módulo

        # Si el numero es NaN
        if math.isnan(number):
            self.bits = [0] + [1]*(ne+nm)
            return "NaN"
            
        # Si el numero es infinito
        if number == float('inf') or number == float('-inf') or modulo > (2-2**(-nm))*2**(2**ne-sesgo-2):
            self.bits[0] = 1 if number < 0 else 0   # Guardo el signo
            self.bits = [self.bits[0]] + [1]*ne + [0]*nm
            return "+inf" if self.bits[0] == 0 else "-inf"

        # Si el numero esta en [-epsilon,+epsilon], lo consideramos 0
        if modulo < 2**(-nm)*2**(1-sesgo): 
            self.bits = [0]*(ne+nm+1)
            return "cero"

        # Subnormales
        if modulo < 2**(1-sesgo):
            expTotal=1-sesgo
            self.bits[1:6]=[0]*5
            mantisa=(modulo/2**expTotal)
        else:
            expTotal = math.floor(math.log2(modulo))
            exp = expTotal + sesgo        
            self.bits[1:6]=exp2bin (exp, ne) # pasar y guardar exp en binario
            mantisa = (modulo/2**expTotal) - 1

        self.bits[6:16]=man2bin (mantisa, nm) # pasar y guardar mantisa en binario
        return "NO"

    def bin2dec(self):
        ne = 5  # Cantidad de Bits de Exponente
        nm = 10 # Cantidad de Bits de Mantisa
        sesgo = 2**(ne-1)-1
        
        if self.bits[1:] == [1]*ne + [0]*nm:        # Caso infinito
            self.d= float('inf') if self.bits[0] == 0 else float('-inf')
            return True

        elif self.bits[1:6] == [1]*ne:         # Caso NaN
            self.d= float('NaN')
            return True

        if self.bits[1:] == [0]*ne + [0]*nm:        # Caso 0
            self.d = float(0)

        elif self.bits[1:6] == [0]*ne:              # Caso Sub-Normal
            mantis = 0
            for i in range(nm):
                mantis += self.bits[i+6]* 2**(-i-1)                
            self.d = (-1)**self.bits[0]*mantis*2**(1-sesgo)

        else:                                       # Caso Normal
            mantis = 1
            for i in range(nm):
                mantis += self.bits[i+6] * 2**(-i-1)
            expo = 0
            for j in range(ne):
                expo += self.bits[j+1] * 2**(ne-j-1)
            self.d = (-1)**self.bits[0]*mantis*2**(expo-sesgo)    

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
def exp2bin (exp, expBits):
    cont = 0
    expb=[]

    if exp > 2**expBits:    # Numero mayor de lo que puedo guardar
        return [1, 1, 1, 1, 1]
        
    while cont<expBits:
        expb = [exp%2] + expb
        exp = exp // 2 
        cont += 1
    return expb    

def man2bin (man, manBits):
    cont = 0
    manb=[]
      
    while cont<manBits:
        man *= 2
        if man>=1:
            manb = manb + [1]
            man -= 1
        else:
            manb = manb + [0]      
        cont += 1

    return manb

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#                             MAIN (TestBench)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def test(numb):
    
    IeeeNumb = binary16(numb)
    IeeeNumb2 = binary16(numb*2)
    res = binary16(0)

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


# Numero positivo
test(4)
print("\n\n")

# Numero negativo
test(-4)
print("\n\n")

# Numero subnormal
test(3e-7)
print("\n\n")

# Numero subnormal negativo
test(-3e-7)
print("\n\n")

# Numero muy cercano a cero -> 0
test(-5e-10)
print("\n\n")

# Numero mayor al mas grande -> inf
test(999999999)
print("\n\n")

# Numero menor al mas chico -> -inf
test(-999999999)
print("\n\n")

# Infinito de float
test(float('+inf'))
print("\n\n")

# Infinito negativo de float
test(float('-inf'))
print("\n\n")

# Not a number de float
test(float('NaN'))
print("\n\n")

# ------------------------------------------------------------------------------
# Preguntas
# ------------------------------------------------------------------------------
    #Suma/Resta puede ser en decimal?
    #Solo numeros normal o tambien subnormales?