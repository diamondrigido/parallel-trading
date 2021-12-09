from typing import List

import pandas as pd

from .indicators import BaseToolIndicator


class BaseDataset:

    df: pd.DataFrame = None
    columns: list = None
    drop_columns: list = None
    indicators: List[BaseToolIndicator]
    data = None

    def __init__(self, data=None):
        self.data = data

    def get_df(self):
        self.load()
        self.get_change_indicators()
        return self.df

    def load(self):
        df = pd.DataFrame(self.data, columns=self.columns)
        df = df.drop(self.drop_columns, axis=1)
        self.df = df

    def get_change_indicators(self):
        indicators = self.indicators

        if indicators is not None:
            for indicator in indicators:
                instance_indicator = indicator(df=self.df)
                instance_indicator.add_data()
                self.df = instance_indicator.df
