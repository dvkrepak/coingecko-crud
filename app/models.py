from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Crypto(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
