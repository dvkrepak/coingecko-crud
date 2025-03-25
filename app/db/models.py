from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Crypto(Base):
    """
    Represents a cryptocurrency record in the database.

    Attributes:
        id (int): Primary key for the crypto record.
        cg_id (str): Unique CoinGecko ID (e.g., "bitcoin").
        symbol (str): The crypto symbol (e.g., "btc").
        name (str): The full name of the cryptocurrency.
        price (float): The current price of the cryptocurrency.
    """
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    cg_id = Column(String, unique=True, index=True)  # coingecko id - for example "bitcoin"
    symbol = Column(String, index=True)  # for example "btc"
    name = Column(String)
    price = Column(Float)
