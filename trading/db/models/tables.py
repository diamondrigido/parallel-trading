from sqlalchemy import Column, String, Float, Integer

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)


class Symbol(BaseModel):
    __tablename__ = "symbol"

    name = Column(String(50))


class StatusSymbol(BaseModel):
    __tablename__ = "status_symbol"

    symbol = Column(String(50))
    price = Column(Float, default=0)
    buying_price = Column(Float, default=0)
    fiat_balance = Column(Float, default=20)
    stop_loss = Column(Float, default=0)
