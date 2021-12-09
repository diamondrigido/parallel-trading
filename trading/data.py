from dataclasses import dataclass


@dataclass
class StatusSymbol:

    symbol: str
    price: float
    buying_price: float
    fiat_balance: float
    status: str
    quantity: float


symbols = [
    "OGNUSDT",
    "RVNUSDT",
    "BNBUSDT",
    "ALGOUSDT",
    "TRXUSDT",
    "DATAUSDT",
    "HIVEUSDT",
    "ZRXUSDT",
    "ICXUSDT",
    "ATOMUSDT",
    "VETUSDT",
    "EOSUSDT",
    "MTLUSDT"
]
symbols_status = [StatusSymbol(symbol, 0, 0, 20, "BUY", 12) for symbol in symbols]

if __name__ == "__main__":
    for symbol_status in symbols_status:
        print(symbol_status.symbol)
