from curses import window
import errno
from turtle import title
from unicodedata import name
from trader import Trader
from alpaca_trade_api import TimeFrame
from websocket import create_connection
from datetime import date
import time
import json
import secret

class Data():
    def __init__(self, trader:Trader):
        self.real_time_data_url = 'wss://stream.data.alpaca.markets/v1beta1/crypto?exchanges=CBSE'
        self.trader = trader

    def auth_bot(self):
        auth_message = {"action":"auth","key": secret.API_KEY, "secret": secret.SECRET_KEY}
        try:
            self._ws.send(json.dumps(auth_message))
            print("Authentication success")
            print("**********************")
        except:
            print("Failure at bot authentication")


    def start_connection(self):
        try:
            self._ws = create_connection(self.real_time_data_url)
            self.auth_bot()
            self.subscribe_to_symbols()
        except:
            print("Failure at web socket connection: ")
    
    def subscribe_to_symbols(self):
        subscription = {"action":"subscribe","trades":[self.trader.symbol], "bars":[self.trader.symbol]}
        try:
            self._ws.send(json.dumps(subscription))
        except:
            print("Failure at subscription")

    def get_symbol_data(self):
            data = json.loads(self._ws.recv())
            return data

    def get_historical_data(self):
        bars = self.trader._api.get_crypto_bars(self.trader.symbol, TimeFrame.Hour,limit=10000).df
        return bars

    def get_historical_average(self):
        bars = self.get_historical_data()
        print(bars["close"].mean())
        return bars['close'].mean()
    
    def get_weekly_average(self):
        barset = self.trader._api.get_crypto_bars(self.trader.symbol, TimeFrame.Day, limit=1000).df
        return barset['close'].mean()


    def get_last_bar(self):
        bar = self.trader._api.get_latest_crypto_bar(self.trader.symbol, exchange="CBSE")
        return bar

    def get_sma(self, nthDayAverage):
        bars = self.trader._api.get_crypto_bars(self.trader.symbol, TimeFrame.Hour).df
        bars = bars[bars.exchange == 'CBSE']
        sma = bars.close.rolling(nthDayAverage).mean()
        print(sma[-1])
        return sma[-1]

        

         
        

            
