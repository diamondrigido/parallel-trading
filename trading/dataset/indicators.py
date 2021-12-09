import pandas as pd


class BaseToolIndicator:
    method_name: str = None
    window_size: int = None

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.close = df["close"]

    def add_data(self):
        raise NotImplementedError

    def set_name(self):
        return f"{self.method_name}_{self.window_size}"


class SMAToolIndicator(BaseToolIndicator):

    def add_data(self):
        column_name = self.set_name()
        self.df[column_name] = self.close.rolling(window=self.window_size).mean()


class RSToolIndicator(BaseToolIndicator):

    method_name = "rs"
    window_size = 14

    def add_data(self):
        column_name = self.set_name()
        self.calculate_avg_gain()
        self.fix_avg_gain()
        self.df["rs_14"] = self.df['avg_gain'] / self.df['avg_loss']

    def calculate_avg_gain(self):
        self.df["close"] = pd.to_numeric(self.df["close"])
        self.df["diff"] = self.df["close"].diff(1)

        self.df["gain"] = self.df["diff"].clip(lower=0).round(2)
        self.df["loss"] = self.df["diff"].clip(upper=0).abs().round(2)

        self.df["avg_gain"] = self.df["gain"].rolling(window=self.window_size,
                                                      min_periods=self.window_size).mean()[:self.window_size + 1]
        self.df["avg_loss"] = self.df["loss"].rolling(window=self.window_size,
                                                      min_periods=self.window_size).mean()[:self.window_size + 1]

    def fix_avg_gain(self):
        for i, row in enumerate(self.df['avg_gain'].iloc[self.window_size + 1:]):
            self.df['avg_gain'].iloc[i + self.window_size + 1] = (self.df['avg_gain'].iloc[i + self.window_size] * (
                    self.window_size - 1) + self.df['gain'].iloc[i + self.window_size + 1]) \
                                                                 / self.window_size

        for i, row in enumerate(self.df['avg_loss'].iloc[self.window_size + 1:]):
            self.df['avg_loss'].iloc[i + self.window_size + 1] = (self.df['avg_loss'].iloc[i + self.window_size] * (
                    self.window_size - 1) + self.df['loss'].iloc[i + self.window_size + 1]) \
                                                                 / self.window_size


class RSIToolIndicator(RSToolIndicator):

    def add_data(self):
        super(RSIToolIndicator, self).add_data()
        column_name = self.set_name()
        self.df[column_name] = 100 - (100 / (1 + self.df["rs_14"]))
