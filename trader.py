# Trader class to handle all trading activity. i.e. buys, sells, account login...
from secret import API_KEY, SECRET_KEY
import alpaca_trade_api as tradeapi


class Trader:

    def __init__(self, symbol):
        # api key
        self._key_id_ = API_KEY
        self._secret_id_ = SECRET_KEY

        self._base_url_ = 'https://paper-api.alpaca.markets'
        self._data_url_ = 'https://data.alpaca.markets'

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
        return self.account.buying_power

    def get_cash(self):
        return self.account.cash

    def is_pattern_day_trader(self):
        return self.account.pattern_day_trader

    def get_day_trade_count(self):
        return self.account.daytrade_count
