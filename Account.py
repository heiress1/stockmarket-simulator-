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