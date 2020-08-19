# Monte Carlo Asset Price Stimulator
# Adapted from:
# http://codereview.stackexchange.com/questions/86273/monte-carlo-asset-price-simulation
# Jack JiaLiang Tian
# 25.01.2016

# Example
#start = 10 dollar price
#sd = 12 in decimal 0.x
#days = 25 
#bins = [40,50,60]
#iterations = 1000
#GAUSS = True # distribution can be gaussian or lognormal

import random

class Trial:
    
    def __init__(self, start, sd, days, bins, iterations, GAUSS):
        
        self.start = start
        self.sd = sd
        self.days = days
        self.bins = bins
        self.iterations = iterations
        self.GAUSS = GAUSS
        self.results = [0] * (len(bins) + 1)
        
    def run(self):
        
        for i in range(self.iterations):
            mc = self.start
            for i in range(self.days):
                if self.GAUSS:
                    mc += random.gauss(0, self.sd)
                else:
                    if random.randint(0,1):
                        mc += random.lognormvariate(0, self.sd)
                    else:
                        mc -= random.lognormvariate(0, self.sd)
                if mc <= 0: # prices can't go below 0
                    mc = 0
        
            for n, bin in enumerate(self.bins): # bin the iteration
                if mc < bin:
                    self.results[n] += 1
                    break
            else:
                self.results[-1] += 1

        
        final = [100 * r / float(self.iterations) for r in self.results]

        return(final)



#if __name__ == '__main__':
    #start = 58 # dollar price
    #sd = 47 #decimal 0.x * 100
    #days = 1 
    #bins = [40, 50, 60]
    #iterations = 1000000
    #GAUSS = True # distribution can be gaussian or lognormal 
    #a = Trial(start, sd, days, bins, iterations, GAUSS).run()
    #print (a)