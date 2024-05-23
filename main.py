import PySimpleGUI as sg
from Account import Account
from Stockmarket import Stockmarket

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
