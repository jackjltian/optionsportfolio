#Black-Scholes Options Pricing Calculator
#for European-typed options.
#Jack JiaLiang Tian
#22.01.2016

import math

#Call options.
class ecall:
    
    def __init__(self, s, k, r, d, v, t):
        self.s = s
        self.k = k
        self.r = r
        self.d = d
        self.v = v
        self.t = float(t)
    
    def price(self):
        d1 = (math.log(self.s/self.k) + (self.r+self.v*self.v/2) * self.t) / (self.v * math.sqrt(self.t))
        d2 = d1 - self.v*math.sqrt(self.t)
        return self.s * CND(d1) - self.k * math.exp(-self.r * self.t) * CND(d2)
    
#Put options.
class eput:
    
    def __init__(self, s, k, r, d, v, t):
        self.s = s
        self.k = k
        self.r = r
        self.d = d
        self.v = v
        self.t = float(t)
        
    def price(self):
        d1 = (math.log(self.s/self.k) + (self.r+self.v*self.v/2) * self.t) / (self.v * math.sqrt(self.t))
        d2 = d1 - self.v*math.sqrt(self.t)
        return self.k * CND(-d2) - self.s * math.exp(-self.r * self.t) * CND(-d1)    


#Normal Calculator, copied from: http://www.espenhaug.com/black_scholes.html
def CND(X):
    (a1,a2,a3,a4,a5) = (0.31938153, -0.356563782, 1.781477937, 
     -1.821255978, 1.330274429)
    L = abs(X)
    K = 1.0 / (1.0 + 0.2316419 * L)
    w = 1.0 - 1.0 / math.sqrt(2*3.14159)*math.exp(-L*L/2.) * (a1*K + a2*K*K + a3*pow(K,3) +
    a4*pow(K,4) + a5*pow(K,5))
    if X<0:
        w = 1.0-w
    return w

#if __name__ == '__main__':
    
    ##Instructions.
    #print('instantiate an option in the following format:')
    #print('examples:')
    #print('name = ecall(s, k, r, delta, sigma, t)')
    #print('name = eput(s, k, r, delta, sigma, t)')
    #print('"name.price()" to calculate price.')
    
    ##Test cases.
    
    #nxp = ecall(1,1,0.1,0.9,0.2,4)
    #fsl = eput(1,1,0.1,0.9,0.2,1)