import math

class binary16:
    def __init__(self, number):
        self.d = float(number)
        self.bits = [0]*16
        self.dec2bin()
        # print("Signo:", self.bits[0])
        # print("Exp:", self.bits[1:6])
        # print("Mantisa:", self.bits[6:16])

    def dec2bin(self):
        ne = 5
        nm = 10
        self.bits[0]= 1 if self.d < 0 else 0    # Guardo el signo
        moduloD = abs(self.d)
        sesgo = 2**(ne-1)-1 
        
        expTotal = 0   

        if moduloD < 2**(1-sesgo):   # Si el numero esta en [-epsilon,+epsilon], lo consideramos 0
            return [0]*(ne+nm+1)
        
        if moduloD > (2-2**(-nm))*2**(2**ne-sesgo-2): # Si el numero es infinito
            return self.bits[0] + [1]*ne + [0]*nm 

        expTotal = math.floor(math.log2(moduloD))
        #TODO: que pasa si expTotal es menor a 2**(ne-1)
        exp = expTotal + sesgo        
        self.bits[1:6]=exp2bin (exp, ne) # pasar y guardar exp en binario

        mantisa = (moduloD/2**expTotal) - 1
        self.bits[6:16]=man2bin (mantisa, nm) # pasar y guardar mantisa en binario


    def identity(self):
        return self.bits

    def negative(self):
        return [1 if self.bits[0]==0 else 0] + self.bits[1:]

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


pruebita = binary16(-0.2)
print(pruebita.bits)
print(pruebita.negative())











# def binaryOfFraction(fraction):
 

#     binary = str()
#     while (fraction):
#         fraction *= 2

#         if (fraction >= 1):
#             int_part = 1
#             fraction -= 1
#         else:
#             int_part = 0
     
#         binary += str(int_part)
 
#     return binary
 

# def floatingPoint(real_no):
 

#     sign_bit = 0
 

#     if(real_no < 0):
#         sign_bit = 1
 

#     real_no = abs(real_no)
 
#     # Converting Integer Part
#     # of Real no to Binary
#     int_str = bin(int(real_no))[2 : ]
 
#     # Function call to convert
#     # Fraction part of real no
#     # to Binary.
#     fraction_str = binaryOfFraction(real_no - int(real_no))
#     ind = int_str.index('1')
#     exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]
#     mant_str = int_str[ind + 1 : ] + fraction_str
#     mant_str = mant_str + ('0' * (23 - len(mant_str)))
 
#     return sign_bit, exp_str, mant_str
 
# # Driver Code
# if __name__ == "__main__":
 
#     sign_bit, exp_str, mant_str = floatingPoint(-2.250000)
#     ieee_32 = str(sign_bit) + '|' + exp_str + '|' + mant_str
#     print("IEEE 754 representation of -2.250000 is :")
#     print(ieee_32)








    #Suma/Resta puede ser en decimal?
    #Solo numeros normal o tambien subnormales?