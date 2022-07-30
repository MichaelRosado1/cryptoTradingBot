from trader import Trader
from data import Data
from strategy import Strategy


def main():
    t = Trader('BTCUSD')

    data_stream = Data(t)
    data_stream.start_connection()
    
    strat = Strategy(t, data_stream)
    strat.start_trading()


if __name__ == '__main__':
    main()
