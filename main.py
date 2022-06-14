from trader import Trader
import time

def main():
    t = Trader('DOGEUSD')

    print(t.get_historical_data())



if __name__ == '__main__':
    main()
