# Trader class to handle all trading activity. i.e. buys, sells, account login...
from secret import API_KEY, SECRET_KEY
from alpaca_trade_api.rest import TimeFrame
import alpaca_trade_api as tradeapi
import json
from datetime import date, datetime


class Trader:

    def __init__(self, symbol):
        # api key
        self._key_id_ = API_KEY
        self._secret_id_ = SECRET_KEY
        self._base_url_ = 'https://paper-api.alpaca.markets'
        self._data_url_ = 'https://data.alpaca.markets'
        self.balance = 0
        self.symbol = symbol
        self.authenticate_bot()

        
    def authenticate_bot(self):
        try:
            self._api = tradeapi.REST(
                self._key_id_,
                self._secret_id_,
                self._base_url_
            )
            self.account = self._api.get_account()
            print('Connection made :)')
        except:
            print('Not able to connect to api')

    def get_buying_power(self):
        try:
            return self.account.buying_power
        except:
            print('error getting buying power')

    def get_cash(self):
        try:
            return float(self.account.cash)
        except:
            print('error geting cash')

    def is_pattern_day_trader(self):
        try:
            return self.account.pattern_day_trader
        except:
            print('error getting is_pattern_day_trader')

    def get_day_trade_count(self):
        try:
            return self.account.daytrade_count
        except:
            print('error getting day trade count')

    def place_order(self, quantity):
        try:
            order = self._api.submit_order(
                symbol=self.symbol,
                qty=quantity,
                side='buy',
                type='market'
            )
            print(f'Order made: {order.symbol} was bought at {order.submitted_at}')
        except:
            print('error placing order')

    def sell_order(self, quantity):
        try:
            order = self._api.submit_order(
                symbol=self.symbol,
                qty=quantity,
                side='sell',
                type='market'
            )
            print(f'Order made: {order.symbol} was sold at {order.submitted_at}')
        except:
            print('error selling order')

    def get_position(self, symbol):
        try:
            return self._api.get_position(symbol)
        except:
            print('Not able to get position on {}', symbol)

    def update_trade_log(self, bar, type_of_trade):
        try:
            data = {}
            bar["type_of_trade"] = type_of_trade

            if (type_of_trade == 'b'):
                self.balance = self.balance - bar['close']
            else:
                self.balance = self.balance + bar['close']

            bar['current_pnl'] = self.balance
            data[str(datetime.now())] = bar 
            with open(f"./data/trades_made_{str(date.today())}.json", "w") as openfile:
                openfile.write(json.dumps(data, indent=4))
        except:
            print('error printing trade log')
