import os.path
import logging
import logging.config

from binance import Client

from .settings import *
from .dataset import BaseDataset, SMAToolIndicator, RSIToolIndicator
from .algorithms import SimpleAlgorithm
from .utils import get_quantity
from .data import symbols_status


# logging.config.fileConfig(os.path.join(BASE_DIR, "settings/logging.conf"))
logger = logging.getLogger("trading_base")


class SMA24(SMAToolIndicator):
    method_name = "sma"
    window_size = 24


class SMA96(SMAToolIndicator):
    method_name = "sma"
    window_size = 96


class RSI(RSIToolIndicator):
    method_name = "rsi"
    window_size = 14


class Dataset(BaseDataset):
    indicators = [SMA24, SMA96, RSI]
    data = None
    columns = ['open time', 'open', 'high', 'low', 'close', 'volume',
               'close time', 'asset', 'number', 'base', 'quote', 'ignore']
    drop_columns = ['high', 'low', 'volume', 'asset', 'number', 'base', 'quote', 'ignore']

    def change_sma(self):
        sma_lst = []
        for indicator in self.indicators:
            if indicator.method_name == "sma":
                sma_lst.append(indicator.window_size)
        sma_lst.sort()
        logger.info("Change SMA column created")
        self.df["change_sma"] = self.df[f"sma_{sma_lst[0]}"] - self.df[f"sma_{sma_lst[1]}"]

    def get_df(self):
        self.df = super(Dataset, self).get_df()
        self.change_sma()
        return self.df


class Algorithm(SimpleAlgorithm):
    columns_use = {
        "sma_24": 10,
        "change_sma": 1,
        "rsi_14": 1,
        "gain": 8,
        "loss": 12,
        "price_for_if": 1
    }


class TradeBotBase:

    client_class = None
    query = None
    dataset_class = Dataset
    algorithm_class = Algorithm
    interval = "15m"
    limit = 1000

    def __init__(self):
        # self.get_db_session()
        self.get_client()

    def get_query(self):
        # self.query = get_all_symbols(self.db_session)
        self.query = symbols_status

    def get_client(self):
        # client = AsyncClient(settings.API_KEY, settings.API_SECRET)
        # self.client = AsyncClientBinance(client)
        self.client_class = Client(API_KEY, API_SECRET)

    # def get_db_session(self):
    #     engine = f"postgresql+asyncpg://{settings.USER_DB}:{settings.PASSWORD_DB}@0.0.0.0:5432/{settings.DB}"
    #     async_engine = create_async_engine(engine, pool_pre_ping=True)
    #     session = AsyncSession(async_engine)
    #     self.db_session = DBSession(session)

    def get_dataset(self, symbol):
        data = self.get_data(symbol)
        dataset = self.dataset_class(data)
        df = dataset.get_df()
        logger.info("DF WAS CREATED SUCCESSFUL")
        return df

    def get_data(self, symbol):
        klines = self.client_class.get_klines(interval=self.interval, symbol=symbol, limit=self.limit)
        logger.info("DATA WAS GOT FROM CLIENT")
        return klines

    def get_trade(self):
        self.get_query()
        for instance in self.query:
            logger.info(f"INSTANCE WAS CREATED. Insance = {instance}")
            df = self.get_dataset(instance.symbol)
            algo = self.algorithm_class(instance.buying_price, instance.status)
            logger.info("ALGORITHM IS CREATED")
            algo.df = df
            logger.info("DF PUT IN ALGORITHM")
            method, value = algo.get_value()
            logger.info(f"Method = {method}  --- Value = {str(value)}")
            if method == "BUY":
                symbol_info = self.client_class.get_symbol_info(instance.symbol)
                quantity = get_quantity(instance.fiat_balance, value, symbol_info)
                param = {
                    "symbol": instance.symbol,
                    "side": method,
                    "type": "LIMIT",
                    "timeInForce": "GTC",
                    "quantity": quantity,
                    "price": str(value)
                }
                instance.quantity = quantity
                instance.status = method
                instance.buying_price = value
                # self.client_class.get_order(**param)
                logger.info(f"BUY {instance.symbol} --- quantity = {quantity} --- value = {value}")
            elif method == "SELL":
                param = {
                    "symbol": instance.symbol,
                    "side": method,
                    "type": "LIMIT",
                    "timeInForce": "GTC",
                    "quantity": instance.quantity - 1,
                    "price": str(value)
                }
                # self.client_class.get_order(**param)
                instance.status = method
                instance.buying_price = value
                logger.info(f"SELL {instance.symbol} --- quantity = {instance.quantity} --- value = {value}")
            else:
                logger.info("NO BUY NO SELL")
                pass

            # self.db_session.commit_session()

            logger.info("Commit session")

        # self.db_session.close_session()

        logger.info("CLOSE SESSION")

        # self.client_class.close()

        logger.info("CLOSE CLIENT")
