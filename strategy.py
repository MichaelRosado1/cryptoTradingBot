import re
from textwrap import indent
from tkinter import W
from trader import Trader
from data import Data
from datetime import date
import json
import time

class Strategy:
    def __init__(self, trader:Trader, data_stream:Data):
        self.trader = trader
        self.ds = data_stream
        self.max_trades = 20 
        self.max_loss_percentage = .025
        self.max_gain_percentage = .025
        self.trading_amount = (self.trader.get_cash() * .25)
        self.trade_qty = 1 

    def start_trading(self):
        cycles = 0
        historicalAverage = self.ds.get_historical_average()
        currently_holding_position = False
        num_of_losing_trades = 0

        num_of_trades = 0
        trades = []

        while (num_of_trades < self.max_trades):
            shortTermSMA = self.ds.get_sma(10)
            cycles += 1
            bar = self.ds.get_last_bar()
            min_bar = {
                "close" : bar.c,
                "high" : bar.h,
                "open" : bar.o,
                "volume" : bar.v, 
                "time" : str(bar.t)
            }

            if (num_of_losing_trades >= 5):
                return


            if (len(trades) > 0 and (((trades[-1] - historicalAverage) / historicalAverage) * 100) <= -5):
                self.trader.update_trade_log(min_bar, "s")
                print('Stop loss hit, selling btc')
                currently_holding_position = False
                num_of_trades += 1
                self.trader.sell_order(self.trade_qty)
                self.trading_amount -= min_bar['close']
                num_of_losing_trades += 1

			# we want to sell when the short term crosses the long term
            if (shortTermSMA > historicalAverage and currently_holding_position):
                self.trader.update_trade_log(min_bar, 's')
                self.trader.sell_order(self.trade_qty)
                currently_holding_position = False
                num_of_trades += 1
                self.trading_amount -= min_bar['close']

            if (shortTermSMA < historicalAverage and not currently_holding_position):
                self.trader.update_trade_log(min_bar, 'b')
                self.trader.place_order(self.trade_qty)
                currently_holding_position = True
                num_of_trades += 1
                self.trading_amount += min_bar['close']
                
            print(f'***** short term sma: {shortTermSMA} long term sma: {historicalAverage} *****')
            time.sleep(60)











           


    
