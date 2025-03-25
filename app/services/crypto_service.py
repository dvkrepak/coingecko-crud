from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db import crud, models
from app.services import coingecko


def list_cryptos(db: Session):
    """
    Retrieve a list of all cryptocurrencies from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[models.Crypto]: A list of all cryptocurrency records.
    """
    return crud.get_all_cryptos(db)


def create_crypto_from_query(db: Session, query: str) -> models.Crypto:
    """
    Create a new crypto record based on a query (symbol or name).

    Args:
        db (Session): The database session.
        query (str): The symbol or name of the cryptocurrency.

    Returns:
        models.Crypto: The created crypto record.
    """
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
    """
    Delete a cryptocurrency record from the database by its CoinGecko ID.

    Args:
        db (Session): The database session.
        cg_id (str): The CoinGecko ID of the cryptocurrency to delete.
    """
    crypto = crud.get_crypto_by_id(db, cg_id.lower())
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    crud.delete_crypto(db, cg_id)


def get_crypto_by_id(db: Session, cg_id: str):
    """
    Retrieve a cryptocurrency record by its CoinGecko ID.

    Args:
        db (Session): The database session.
        cg_id (str): The CoinGecko ID of the cryptocurrency.

    Returns:
        models.Crypto: The requested crypto record.
    """
    crypto = crud.get_crypto_by_id(db, cg_id.lower())
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return crypto


def update_crypto_fields(db: Session, cg_id: str, fields: dict):
    """
    Update specific fields of a cryptocurrency record.

    Args:
        db (Session): The database session.
        cg_id (str): The CoinGecko ID of the cryptocurrency to update.
        fields (dict): The fields to update with new values.

    Returns:
        models.Crypto: The updated crypto record.
    """
    updated = crud.update_crypto(db, cg_id.lower(), fields)
    if not updated:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return updated


def update_crypto_price(db: Session, crypto, new_price: float):
    """
    Update the price of a cryptocurrency record.

    Args:
        db (Session): The database session.
        crypto (models.Crypto): The cryptocurrency to update.
        new_price (float): The new price of the cryptocurrency.

    Returns:
        models.Crypto: The updated crypto record.
    """
    return crud.update_crypto_price(db, crypto, new_price)
