class binary16:
  def __init__(self, number):
    self.d = float(number)
    self.bits = self.dec2bin()

    def dec2bin(self):
        # exponente= [0,0,0,0,0]; mantisa=[0,0,0,0,0, 0,0,0,0,0]
        ne=5
        signo = 1 if self.d < 0 else 0
        sesgo = 2**(ne-1)-1 
        
        expTotal = 0
        if abs(self.d) > 2:
            while self.d/2**expTotal < 2: #REVISAR: condicion
                expTotal += 1 
    
        if abs(self.d) < 0.5:
            while self.d/2**expTotal < 2: #REVISAR: condicion
                expTotal += 1

        exp = expTotal + sesgo
        #pasar exp a binario

        mantisa = self.d/2**expTotal - 1 
        #pasar mantisa a binario
        while number




    # def dec2bin(self):
    # binary = [] 
    # while self.d > 0:
    #     binary = str(self.d % 2) + binary
    #     self.d = self.d // 2
    # return binary

















def binaryOfFraction(fraction):
 

    binary = str()
    while (fraction):
        fraction *= 2

        if (fraction >= 1):
            int_part = 1
            fraction -= 1
        else:
            int_part = 0
     
        binary += str(int_part)
 
    return binary
 

def floatingPoint(real_no):
 

    sign_bit = 0
 

    if(real_no < 0):
        sign_bit = 1
 

    real_no = abs(real_no)
 
    # Converting Integer Part
    # of Real no to Binary
    int_str = bin(int(real_no))[2 : ]
 
    # Function call to convert
    # Fraction part of real no
    # to Binary.
    fraction_str = binaryOfFraction(real_no - int(real_no))
    ind = int_str.index('1')
    exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]
    mant_str = int_str[ind + 1 : ] + fraction_str
    mant_str = mant_str + ('0' * (23 - len(mant_str)))
 
    return sign_bit, exp_str, mant_str
 
# Driver Code
if __name__ == "__main__":
 
    sign_bit, exp_str, mant_str = floatingPoint(-2.250000)
    ieee_32 = str(sign_bit) + '|' + exp_str + '|' + mant_str
    print("IEEE 754 representation of -2.250000 is :")
    print(ieee_32)