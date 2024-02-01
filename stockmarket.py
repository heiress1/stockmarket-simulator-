import pandas as pd
import yfinance as yf
from datetime import date, timedelta
from matplotlib import pyplot as plt
from yahoo_fin import stock_info

class Account():
    """
    manages bank account by depositing and withdrawing money
   
    Attributes:
        money: amount of money in bank account
    """
    def __init__(self, money ):
        self.money = money
       
    def __repr__(self):
        return "money " + str(self.money)
       
    def withdraw(self, amount):
        """
        withdraws money from bank account
       
        Parameters
        ----------
        amount: int
            amount of money being withdrawn
           
        Returns
        -------
        integer
            amount of money in account after withdrawing money
        """
        self.money -= amount
        return self.money
       
    def deposit(self, amount):
        """
        deposits money into bank account
       
        Parameters
        ----------
        amount: int
            amount of money being deposited
           
        Returns
        -------
        integer
            amount of money in account after depositing money
        """
        self.money += amount
        return self.money
       
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
   
       

import PySimpleGUI as sg
def main():
    """
    creates gui layout
    calls and creates all objects and methods for Stockmarket and Account classes
   
    """
    #creates Account object
    aires = Account(1000000)
    layout = [ [sg.Text("Stock Simulator")],
              [sg.Text("Enter Ticker"), sg.Input(key="ticker", size=(10,5)), sg.Button("Search"), sg.Button("Plot")],
              [sg.Text("Stock Price ($)"), sg.Text("", key = "price"), sg.Button("Buy"), sg.Input(key="buy", size=(4,5)), sg.Button("Sell"), sg.Input(key="sell", size=(4,5))],
              [sg.Text("Balance ($): "), sg.Text(aires.money, key = "balance")],
              [sg.Text("", key = "message")],
              [sg.Text("Portfolio")],
              [sg.Text("", key = "portfolio")]
             
             ]

    window = sg.Window("Stock Market", layout, element_justification='c')

    #creates stock object 
    stock = Stockmarket()
    while True:
       
        event, values = window.read()
        
        #close program
        if event == sg.WIN_CLOSED:
            break
        
        #updates the portfolio on the GUI
        window["portfolio"].update(stock.portfolio)
       
        #what happens when the button Search is pressed  
        if event == 'Search' and not values["ticker"] =="":
            
            #shows the price of the stock
            window["price"].update(round(stock_info.get_live_price(values["ticker"]),2))
        
        #plots the graph of the stock
        elif event == "Plot":
            if values["ticker"] != "":
                #clears of any error messages
                window["message"].update("")
                
                #creates graph 
                stock.create_graphs("red", values["ticker"] + " Performance", values["ticker"])
            else:
                window["message"].update("No ticker was entered")
        #buy stock
        elif event == "Buy":
            if values["buy"] != "" and aires.money >= round(stock_info.get_live_price(values["ticker"]),2):
                #clears error messages
                window["message"].update("")
                
                #adds stocks to portfolio
                stock.addStocks(values["buy"], values["ticker"])
                
                #buys to stock
                bank = stock.buy(aires, values["buy"], values["ticker"])
                
                #updates portfolio on GUI
                window["portfolio"].update(stock.portfolio)
                
                #updates amount of money left shows in GUI
                window["balance"].update(bank)
            #shows error message
            else:
                window["message"].update("Cannot buy stock, insufficient funds or no amount was entered")
        
        #when selling stock
        elif event == "Sell":
            if values["sell"] != "" and stock.portfolio[values["ticker"]] >= int(values["sell"]):
                #clears error messages
                window["message"].update("")
                
                #sells stocks and returns money to bank
                bank = stock.sell(aires, values["sell"], values["ticker"])
                
                #Updates money in bank shown on GUI
                window["balance"].update(bank)
                
                #removes stocks from portfolio
                stock.subStocks(values["sell"], values["ticker"])
                
                #updates portfolio on GUI
                window["portfolio"].update(stock.portfolio)
            else:
                window["message"].update("no amount was entered or you don't have enough of stocks to to sell")  
        #what happens Search button is pressed without ticker entered
        else:
            window["message"].update("no ticker was entered")
main()
