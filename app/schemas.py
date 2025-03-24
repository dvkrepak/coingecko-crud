from pydantic import BaseModel, ConfigDict


class CryptoBase(BaseModel):
    symbol: str


class CryptoCreate(CryptoBase):
    pass


class Crypto(CryptoBase):
    id: int
    name: str
    price: float

    class Config:
        model_config = ConfigDict(from_attributes=True)
