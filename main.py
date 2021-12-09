from trading.base import TradeBotBase
import datetime

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    trade = TradeBotBase()
    trade.get_trade()
    print("TIME: ", datetime.datetime.now() - start_time)

