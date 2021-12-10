import logging
import datetime
import logging.config

from trading.base import TradeBotBase
from trading.settings import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("time_process")


if __name__ == "__main__":
    num_proc = [1, 2, 3, 4]
    for num in num_proc:
        start_time = datetime.datetime.now()
        trade = TradeBotBase()
        trade.get_trade(num)
        logger.debug(f" Count processes = {num}. Time: {datetime.datetime.now() - start_time}")

