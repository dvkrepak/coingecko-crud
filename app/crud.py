from sqlalchemy.orm import Session

from app import models


def get_crypto_by_id(db: Session, cg_id: str):
    return db.query(models.Crypto).filter(models.Crypto.cg_id == cg_id.lower()).first()


def create_crypto(db: Session, crypto: models.Crypto):
    db.add(crypto)
    db.commit()
    db.refresh(crypto)
    return crypto


def get_all_cryptos(db: Session):
    return db.query(models.Crypto).all()


def update_crypto(db: Session, cg_id: str, updated_fields: dict):
    crypto = get_crypto_by_id(db, cg_id)
    if not crypto:
        return None
    for key, value in updated_fields.items():
        setattr(crypto, key, value)
    db.commit()
    db.refresh(crypto)
    return crypto


def delete_crypto(db: Session, cg_id: str):
    crypto = get_crypto_by_id(db, cg_id)
    if not crypto:
        return None
    db.delete(crypto)
    db.commit()
    return crypto


def update_crypto_price(db: Session, crypto: models.Crypto, new_price: float):
    crypto.price = new_price
    db.commit()
    db.refresh(crypto)
    return crypto
