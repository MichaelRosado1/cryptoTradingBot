from trader import Trader
import time

def main():
    t = Trader('DOGEUSD')
    t.place_order(1)
    time.sleep(10)    
    t.sell_order(1)



if __name__ == '__main__':
    main()
