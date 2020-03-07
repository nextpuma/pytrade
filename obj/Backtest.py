# Other imports
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from obj.Trade import Trade

class Backtest:
    def __init__(self, starting_amount, start_datetime, end_datetime, strategy, verbose):
        self.verbose:bool = verbose
        self.start:int = starting_amount
        self.num_trades:int = 0
        self.profitable_trades:int = 0
        self.amount:int = self.start
        self.startTime = start_datetime
        self.endTime = end_datetime
        self.strategy = strategy
        self.trades = []
        self.run_backtest()
        self.print_results()


    def run_backtest(self):
        time = self.strategy.time[self.strategy.tradeCoins[-1]]
        point_finder = 0
        strategy_result = self.strategy.strategy_result
        #Finds the first cross point within the desired backtest interval
        while strategy_result[point_finder][0] < self.startTime:
            point_finder += 1
        #Initialize to not buy
        active_buy = False
        buy_price = 0
        #Runs through each kline
        for i in range(len(self.strategy.klines[self.strategy.tradeCoins[-1]])):
            if point_finder > len(strategy_result)-1:
                break
            #If timestamp is in the interval, check if strategy has triggered a buy or sell
            if time[i] > self.startTime and time[i] < self.endTime:
                if(time[i] == strategy_result[point_finder][0]):
                    if strategy_result[point_finder][3] == 'BUY':
                        active_buy = True
                        buy_price = float(strategy_result[point_finder][4])
                        self.trades.append(['BUY', buy_price, strategy_result[point_finder][5]])
                    if strategy_result[point_finder][3] == 'SELL' and active_buy == True:
                        active_buy = False
                        bought_amount = amount / buy_price
                        self.num_trades += 1
                        if(float(strategy_result[point_finder][4]) > buy_price):    
                            self.profitable_trades += 1
                        amount = bought_amount * float(strategy_result[point_finder][4])
                        self.trades.append(['SELL', float(strategy_result[point_finder][4]), strategy_result[point_finder][5]])
                    point_finder += 1
        self.amount = amount

    def print_results(self):
        print(f"\nTrade coins: {self.strategy.tradeCoins}")
        print(f"Indicator: {self.strategy.indicator}")
        print(f"Strategy: {self.strategy.strategy}")
        print(f"Interval: {self.strategy.interval}")
        print(f"Ending amount: {str(self.amount)}")
        print(f"Number of Trades: {str(self.num_trades)}")
        if self.num_trades > 0:
            print(f"Percentage of Profitable Trades: {str(self.profitable_trades / self.num_trades * 100)}%")
        print(f"{str(self.amount / self.start * 100)}% of starting amount")
        if self.verbose:
            for i in range(len(self.trades)):
                if i > 0 and self.trades[i][0] == "SELL":
                    print(f"{self.trades[i][0]} {self.trades[i][2]} at {str(self.trades[i][1])} | {int(((self.trades[i][1] / self.trades[i - 1][1]) * 100) - 100)}%")
                else:
                    print(f"{self.trades[i][0]} {self.trades[i][2]} at {str(self.trades[i][1])}")
