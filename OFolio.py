#OFolio.py
#Application developed for options trading based on stock information from NASDAQ.
#Jack JiaLiang Tian
#22.01.2016

import math
from mc import Trial
from bs import ecall
from bs import eput
from bt import aOption
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import time
import datetime
from datetime import tzinfo, timedelta, datetime
from OFolio import *
import os
from os import listdir
from os.path import isfile, join
import pickle


class Asset():
    
    def __init__(self, symbol, otype, t):  
        self.symbol = symbol #stock symbol to be looked up on NASDAQ.com
        self.otype = otype # call or put option type
        self.t = float(t) # time until expiry in days
        json = urlopen("http://www.nasdaq.com/symbol/" + self.symbol).read() #opens the NASDAQ url and saves it
        soup = BeautifulSoup(json, "html.parser") # saves nasdaq html as a JSON file.
        self.sigma = float(soup.find(id="beta").parent.parent.contents[3].text) # volatility
        self.spot = float(soup.find(id="qwidget_lastsale").contents[0][1:]) # current price of stock on NASDAQ.com
        self.bins = [40, 50, 60] # random numbers used in Monte-Carlo
        self.iterations = 9999 # number of iterations in Monte-Carlo
        self.GAUSS = True # distribution can be gaussian or lognormal        
        self.strike = Trial(float(self.spot), float(self.sigma * 100), int(self.t), self.bins, int(self.iterations), bool(self.GAUSS)).run()[-1] #Monte-Carlo hypothetical Strike price; using the last and highest price.
        self.r = 0.5 # Tresury bill rate (Assumed annual constant)
        self.delta = float(soup.find(id="current_yield").parent.parent.contents[3].text[:-1])/100 #Dividend yield rate
        self.u = 2.71828** (self.sigma * math.sqrt(self.t/365)) # binomial tree u factor
        self.d = 1/self.u # binomial tree d factor
        self.oprice = self.price() #option price
        self.sdate = datetime.today() #date instantiated
        self.edate = datetime.today() + timedelta(days = self.t) #calculate date of expiry
        self.current_date = datetime.today()
        self.current_spot = self.spot
    
    def price(self):
        if self.otype == "ecall":
            return ecall(self.spot, self.strike, self.r, self.delta, self.sigma, self.t).price()
        elif self.otype == "eput":
            return eput(self.spot, self.strike, self.r, self.delta, self.sigma, self.t).price()
        elif self.otype == "acall":
            return aOption(self.spot, self.u, self.d, self.r, self.t, self.strike).price()
        elif self.otype == "aput":
            return aOption(self.strike, self.u, self.d, self.r, self.t, self.spot).price()
            
        
    def save(self, filename):
            with open(filename, 'wb') as output:
                pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)  
                
    def update(self):
        json = urlopen("http://www.nasdaq.com/symbol/" + self.symbol).read() #opens the NASDAQ url and saves it
        soup = BeautifulSoup(json, "html.parser") # saves nasdaq html as a JSON file.        
        self.current_spot = float(soup.find(id="qwidget_lastsale").contents[0][1:])
        self.t -= 1/365
        if (self.t == 0):
            pass
        
            
if __name__ == '__main__':

    def main():
        
        #Instructions: instantiate Asset objects in the following format...
        # name = Asset(stock symbol, type, days until expiry)
        stock_symbol = "nxpi"  #Sub in the intended stock symbol. 
        t = 3 # time in days.
        a = Asset(stock_symbol, "eput", t) #.save("nxpieput365")
        b = Asset(stock_symbol, "ecall", t) #.save("nxpiecall365")
        c = Asset(stock_symbol, "aput", t) # t > 365
        d = Asset(stock_symbol, "acall", t) # t > 365
        #.save('filename')to save objects unto computer
        
        root = Tk()
        text = Text(root)
        
        #European put
        text.insert(INSERT, a.symbol,)
        text.insert(INSERT, ", ")
        
        text.insert(INSERT, a.otype, " , " )
        text.insert(INSERT, ", ")
        
        text.insert(INSERT, a.edate, ": ")
        text.insert(INSERT, ", ")
        
        text.insert(INSERT, math.floor(a.spot), ", ")
        text.insert(INSERT, ", ")
        text.insert(INSERT, math.floor(a.strike), ", ")
        text.insert(INSERT, ", ")
        
        text.insert(END, a.oprice)
        
        
        text.pack()
        
        #European call
        text2 = Text(root)
        
        text2.insert(INSERT, b.symbol,)
        text2.insert(INSERT, ", ")
        
        text2.insert(INSERT, b.otype, " , " )
        text2.insert(INSERT, ", ")
        
        text2.insert(INSERT, b.edate, ": ")
        text2.insert(INSERT, ", ")
        
        text2.insert(INSERT, math.floor(b.spot), ", ")
        text2.insert(INSERT, ", ")
        text2.insert(INSERT, math.floor(b.strike), ", ")
        text2.insert(INSERT, ", ")
        
        text2.insert(END, b.oprice)        
        
        text2.pack()
        
        root.mainloop()        
    
    main()