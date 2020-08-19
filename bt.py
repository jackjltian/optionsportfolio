#Binomial Tree Options Pricing Calculator
#for American-typed options.
#Adapted from: http://stackoverflow.com/questions/15100246/python-binomial-option-pricing-code
#Jack JiaLiang Tian
#22.01.2016

import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

class aOption():

    def __init__(self,s0,u,d,r,t,strike):
        self.s0=s0
        self.u=u
        self.d=d
        self.r=r
        self.t= int(t / 365)
        self.strike=strike

    def price(self):
        q = (self.r - self.d) / (self.u - self.d)
        prc = 0
        temp_stock = 0
        temp_payout = 0
        for x in range(1,self.t+1):
            temp_stock = self.strike*(self.u**(4-x))*(self.d**(x-1))
            temp_payout = max(temp_stock-self.strike,0)
            prc += nCr(self.t,x-1)*(q**(4-x))*((1-q)**(x-1))*temp_payout
        prc = prc / (self.r**self.t)
        return prc


#newOption = aOption(100,1.07,0.93458,1.01,2,110)
#print (newOption.price())