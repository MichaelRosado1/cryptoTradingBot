from trader import Trader
from data import Data
import threading

def main():
    t = Trader('DOGEUSD')

    data_stream = Data(t)
    data_stream.start_connection()
    data_stream.get_symbol_data()

if __name__ == '__main__':
    main()
