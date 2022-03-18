# ------------------------------------------------------------------------------
#  @file     +PuntoFlotante.py+
#  @brief    +Implemente del punto flotante IEEE 754 de 16 bits+
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
        self.d = float(number)
        self.bits = [0]*16
        self.dec2bin()
        # FOR DEBUG
        # print("Signo:", self.bits[0])
        # print("Exp:", self.bits[1:6])
        # print("Mantisa:", self.bits[6:16])

    def dec2bin(self):
        ne = 5  # Cantidad de Bits de Exponente
        nm = 10 # Cantidad de Bits de Mantisa
        self.bits[0] = 1 if self.d < 0 else 0    # Guardo el signo
        moduloD = abs(self.d)
        sesgo = 2**(ne-1)-1 
        expTotal = 0   

        # Si el numero esta en [-epsilon,+epsilon], lo consideramos 0
        if moduloD < 2**(1-sesgo):  
            return [0]*(ne+nm+1)
        
        # Si el numero es infinito
        if moduloD > (2-2**(-nm))*2**(2**ne-sesgo-2):
            self.bits[0] = 1 if self.d < 0 else 0    #TODO: No se porque lo tengo que repetir (Nico)  
            for i in range(0, ne): 
                self.bits[i+1] = 1  # Todo el exponente debe ser 1
            return self.bits


        expTotal = math.floor(math.log2(moduloD))
        #TODO: que pasa si expTotal es menor a 2**(ne-1)
        exp = expTotal + sesgo        
        self.bits[1:6]=exp2bin (exp, ne) # pasar y guardar exp en binario

        mantisa = (moduloD/2**expTotal) - 1
        self.bits[6:16]=man2bin (mantisa, nm) # pasar y guardar mantisa en binario

    def identity(self):
        return self.bits

    # Multiplicación por -1
    def negative(self):
        return [1 if self.bits[0]==0 else 0] + self.bits[1:]

    #TODO: SUMA, RESTA y ¿MULTIPLICACION +1?

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
    # return exp2bin(exp//2) + [exp%2] if exp>1 else [exp]

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
    print('El número:', numb, '-> IEEE754: ', IeeeNumb.bits)
    #print(IeeeNumb.negative())

while True:
    print("Write a number:", end="")
    var = input()
    test(var)


# ------------------------------------------------------------------------------
# Preguntas
# ------------------------------------------------------------------------------
    #Suma/Resta puede ser en decimal?
    #Solo numeros normal o tambien subnormales?