from trader import Trader
from websocket import create_connection
import json
import pprint
import secret

class Data():
    def __init__(self, trader:Trader):
        self.real_time_data_url = 'wss://stream.data.alpaca.markets/v1beta1/crypto?exchanges=ERSX,FTXU'
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
        subscription = {"action":"subscribe","trades":[self.trader.symbol], "quotes": [self.trader.symbol], "bars":[self.trader.symbol]}
        try:
            self._ws.send(json.dumps(subscription))
        except:
            print("Failure at subscription")

    def get_symbol_data(self):
            data = json.loads(self._ws.recv())
            pprint.pprint(data)
            print("******************")



        

         
        

            
