from typing import Optional

from pydantic import BaseModel, ConfigDict


class CryptoBase(BaseModel):
    symbol: str


class CryptoCreate(CryptoBase):
    pass


class Crypto(CryptoBase):
    cg_id: str
    symbol: str
    name: str
    price: float

    class Config:
        model_config = ConfigDict(from_attributes=True)


class CryptoUpdate(BaseModel):
    # No update for symbol as it is the primary key
    name: Optional[str] = None
    price: Optional[float] = None
