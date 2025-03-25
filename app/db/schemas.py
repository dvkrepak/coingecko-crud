from typing import Optional

from pydantic import BaseModel, ConfigDict


class CryptoBase(BaseModel):
    """
    Base model for cryptocurrency data, shared between create and update models.

    Attributes:
        symbol (str): The symbol of the cryptocurrency (e.g., "btc").
    """
    symbol: str


class CryptoCreate(CryptoBase):
    """
    Model for creating a new cryptocurrency entry.

    Inherits from CryptoBase.
    """
    pass


class Crypto(CryptoBase):
    """
    Full model representing a cryptocurrency record with additional fields.

    Attributes:
        cg_id (str): The unique CoinGecko ID of the cryptocurrency (e.g., "bitcoin").
        symbol (str): The symbol of the cryptocurrency (e.g., "btc").
        name (str): The full name of the cryptocurrency.
        price (float): The current price of the cryptocurrency.
    """
    cg_id: str
    symbol: str
    name: str
    price: float

    class Config:
        model_config = ConfigDict(from_attributes=True)


class CryptoUpdate(BaseModel):
    """
    Model for updating cryptocurrency fields.

    Fields:
        name (Optional[str]): The updated name of the cryptocurrency.
        price (Optional[float]): The updated price of the cryptocurrency.
    """
    # No update for symbol as it is the primary key
    name: Optional[str] = None
    price: Optional[float] = None
