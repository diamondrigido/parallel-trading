from typing import Dict, Union
import pandas as pd


class BaseAlgorithm:
    df = None
    columns_use: dict = {}
    dct_values: Dict[str, Union[int, list, pd.Series]] = None

    def __init__(self, start_price, status):
        self.start_price = start_price
        self.status = status

    def create_values(self):
        dct_values = {}
        self.df = self.df.dropna()
        for key, value in self.columns_use.items():
            if key == "price_for_if":
                dct_values[key] = self.df["close"].tail(value).values[0]
            else:
                dct_values[key] = self.df[key].tail(value).values

        self.dct_values = dct_values

    def buy_method(self):
        raise NotImplementedError

    def sell_method(self):
        raise NotImplementedError

    def get_value(self):
        self.create_values()
        if self.status == "SELL":
            if self.buy_method():
                method = "BUY"
                value = self.dct_values["price_for_if"]
            else:
                method = None
                value = self.dct_values["price_for_if"]
        else:
            if self.sell_method():
                method = "SELL"
                value = self.dct_values["price_for_if"]
            else:
                method = None
                value = self.dct_values["price_for_if"]

        return method, value


class SimpleAlgorithm(BaseAlgorithm):
    def sell_method(self):
        return True if self.dct_values["price_for_if"] > 1.1 * self.start_price else False

    def buy_method(self):
        return True if self.dct_values["rsi_14"] < 20 else False
