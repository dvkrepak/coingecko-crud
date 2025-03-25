from sqlalchemy.orm import Session
from app.db import models


def get_crypto_by_id(db: Session, cg_id: str):
    """
    Retrieve a crypto record by its CoinGecko ID.

    Args:
        db (Session): The database session.
        cg_id (str): The CoinGecko ID of the crypto.

    Returns:
        models.Crypto: The crypto record, or None if not found.
    """
    return db.query(models.Crypto).filter(models.Crypto.cg_id == cg_id.lower()).first()


def create_crypto(db: Session, crypto: models.Crypto):
    """
    Add a new crypto record to the database.

    Args:
        db (Session): The database session.
        crypto (models.Crypto): The crypto object to add.

    Returns:
        models.Crypto: The created crypto object.
    """
    db.add(crypto)
    db.commit()
    db.refresh(crypto)
    return crypto


def get_all_cryptos(db: Session):
    """
    Retrieve all crypto records from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[models.Crypto]: A list of all crypto records.
    """
    return db.query(models.Crypto).all()


def update_crypto(db: Session, cg_id: str, updated_fields: dict):
    """
    Update specific fields of a crypto record.

    Args:
        db (Session): The database session.
        cg_id (str): The CoinGecko ID of the crypto to update.
        updated_fields (dict): A dictionary of fields to update with their new values.

    Returns:
        models.Crypto: The updated crypto record, or None if the crypto was not found.
    """
    crypto = get_crypto_by_id(db, cg_id)
    if not crypto:
        return None
    for key, value in updated_fields.items():
        setattr(crypto, key, value)
    db.commit()
    db.refresh(crypto)
    return crypto


def delete_crypto(db: Session, cg_id: str):
    """
    Delete a crypto record by its CoinGecko ID.

    Args:
        db (Session): The database session.
        cg_id (str): The CoinGecko ID of the crypto to delete.

    Returns:
        models.Crypto: The deleted crypto record, or None if not found.
    """
    crypto = get_crypto_by_id(db, cg_id)
    if not crypto:
        return None
    db.delete(crypto)
    db.commit()
    return crypto


def update_crypto_price(db: Session, crypto: models.Crypto, new_price: float):
    """
    Update the price of a specific crypto.

    Args:
        db (Session): The database session.
        crypto (models.Crypto): The crypto record to update.
        new_price (float): The new price for the crypto.

    Returns:
        models.Crypto: The crypto record with the updated price.
    """
    crypto.price = new_price
    db.commit()
    db.refresh(crypto)
    return crypto
