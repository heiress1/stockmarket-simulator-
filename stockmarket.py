import pandas as pd
import yfinance as yf
from datetime import date, timedelta
from matplotlib import pyplot as plt
from yahoo_fin import stock_info

class Stockmarket():
    """
    stimulates a stockmarket that allows users to invest in stocks
    look at stock graphs
   
    Attributes:
        ticker: the ticker of the stock
    """

    def __init__(self):       
        self.portfolio = {}
       
    def addStocks(self, num, ticker):
        """
        adds stocks to portfolio when buying stocks
        
        Parameters
        ----------
        num: string
            number of stocks to be added to portfolio
        ticker: string
            the name of the ticker
            
        Returns
        -------
            nothing       
        """
        #if ticker is in portfolio already 
        if ticker in self.portfolio:
            self.portfolio[ticker] += int(num)
        #if ticker is not already in portfolio
        else:
            self.portfolio[ticker] = int(num)
           
    def subStocks(self, num, ticker):
        """
        removes stocks from portfolio when selling stocks
        
        Parameters
        ----------
        num: string
            the number of stocks to be removed from portfolio
        ticker: string
            the name of the ticker
            
        Returns
        ------
            nothing
        """
        self.portfolio[ticker] -= int(num)
       
    def create_graphs(self, colour, title, ticker):
        """
        creates a line graph of a stock
       
        Parameters
        ----------
        colour: string
            the colour of the line graph
        title: string
            the name of the graph
           
        Returns
        -------
             nothing
        """
        #creates the start date of the graph a year from now  
        self.start = date.today() - timedelta(days = 365)
        self.start.strftime('%Y-%m-%d')
       
        #creates the end date
        self.end = date.today()
        self.end.strftime('%Y-%m-%d')
        self.asset = pd.DataFrame(yf.download(ticker, start=self.start, end=self.end)['Adj Close'])
       
        #plots the stock graph
        plt.plot(self.asset, color=colour, linewidth=2)
        plt.title(title)
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.show()
       
    def buy(self, account, numStocks, ticker):
        """
        buy stocks
        withdraws money from bank account
       
        Parameters
        ----------
        account: object
            account object to withdraw money from when buying stocks
        numStocks: string
            number of stocks to buy
           
        Returns
        -------
        integer
            money left in account after buying
        """
        money = (round(stock_info.get_live_price(ticker),2)) * int(numStocks)
       
        return account.withdraw(money)
   
    def sell(self, account, numStocks, ticker):
        """
        sell stocks
        deposites money back to bank account
       
        Parameters
        ----------
        account: object
            account object to deposit money when selling stocks
        numStocks: string
            number of stocks to sell
           
        Returns
        -------
        integer
            money in bank account after selling
        """
        money = (round(stock_info.get_live_price(ticker),2)) * int(numStocks)
        return account.deposit(money)