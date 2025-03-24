from sqlalchemy.orm import Session
from . import models


def get_crypto_by_symbol(db: Session, symbol: str):
    return db.query(models.Crypto).filter(models.Crypto.symbol == symbol).first()


def create_crypto(db: Session, crypto: models.Crypto):
    db.add(crypto)
    db.commit()
    db.refresh(crypto)
    return crypto


def get_all_cryptos(db: Session):
    return db.query(models.Crypto).all()
