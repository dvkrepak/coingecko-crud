from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db import crud, models
from app.services import coingecko


def list_cryptos(db: Session):
    return crud.get_all_cryptos(db)


def create_crypto_from_query(db: Session, query: str) -> models.Crypto:
    data = coingecko.fetch_crypto_data(query)
    if not data:
        raise HTTPException(status_code=404, detail=f"Symbol or name '{query}' not found on Coingecko")

    cg_id = data["id"].lower()
    if crud.get_crypto_by_id(db, cg_id):
        raise HTTPException(status_code=400, detail=f"Crypto '{cg_id}' already exists")

    return crud.create_crypto(db, models.Crypto(
        cg_id=cg_id,
        symbol=data["symbol"].lower(),
        name=data["name"],
        price=data["price"]
    ))


def delete_crypto(db: Session, cg_id: str):
    crypto = crud.get_crypto_by_id(db, cg_id.lower())
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    crud.delete_crypto(db, cg_id)


def get_crypto_by_id(db: Session, cg_id: str):
    crypto = crud.get_crypto_by_id(db, cg_id.lower())
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return crypto


def update_crypto_fields(db: Session, cg_id: str, fields: dict):
    updated = crud.update_crypto(db, cg_id.lower(), fields)
    if not updated:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return updated


def update_crypto_price(db: Session, crypto, new_price: float):
    return crud.update_crypto_price(db, crypto, new_price)
