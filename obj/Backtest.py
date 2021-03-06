# Other imports
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from obj.Trade import Trade

class Backtest:
    def __init__(self, starting_amount, strategy, verbose):
        self.verbose:bool = verbose
        self.start:int = starting_amount
        self.num_trades:int = 0
        self.profitable_trades:int = 0
        self.amount:int = self.start
        self.strategy = strategy
        self.trades = []
        self.run_backtest()
        self.print_results()


    def run_backtest(self):
        amount = self.start
        buy_price = 0
        #Runs through each kline

        for trade in self.strategy.trades:

            if trade.action == 'BUY':
                buy_price = float(trade.price)

            if trade.action == 'SELL':
                bought_amount = amount / buy_price
                if(float(trade.price) > buy_price):    
                    self.profitable_trades += 1
                amount = bought_amount * float(trade.price)

        self.amount = amount

    def print_results(self):
        print(f"Trade coins: {self.strategy.tradeCoins}")
        print(f"Indicator: {self.strategy.indicator}")
        print(f"Strategy: {self.strategy.strategy}")
        print(f"Interval: {self.strategy.interval}")
        print(f"Ending amount: {str(self.amount)}")
        print(f"{(self.amount / self.start) * 100}% of starting amount")
        print(f"Number of Trades: {len(self.strategy.trades)}")
        if len(self.strategy.trades) > 0:
            print(f"Percentage of profitable sells: {(self.profitable_trades / (len(self.strategy.trades) / 2)) * 100}%")
            if self.verbose:
                for trade in self.strategy.trades:
                    print(f"{trade.time} | {trade.action} {trade.trade_coin} at {trade.price}")
