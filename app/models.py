from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Crypto(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    cg_id = Column(String, unique=True, index=True)     # coingecko id - for example "bitcoin"
    symbol = Column(String, index=True)                 # for example "btc"
    name = Column(String)
    price = Column(Float)
