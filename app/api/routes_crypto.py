import logging
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import schemas
from app.services import crypto_service, coingecko

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=list[schemas.Crypto])
def read_cryptos(db: Session = Depends(get_db)):
    """
    Retrieve a list of all cryptos from the database.

    Args:
        db (Session): The database session dependency.

    Returns:
        list[schemas.Crypto]: A list of crypto items.
    """
    cryptos = crypto_service.list_cryptos(db)
    logger.info(f"Retrieved {len(cryptos)} cryptos")
    return cryptos


@router.get("/{cg_id}", response_model=schemas.Crypto)
def read_crypto(cg_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific crypto by its CoinGecko ID.

    Args:
        cg_id (str): The CoinGecko ID of the crypto.
        db (Session): The database session dependency.

    Returns:
        schemas.Crypto: The requested crypto object.
    """
    crypto = crypto_service.get_crypto_by_id(db, cg_id)
    logger.info(f"Retrieved crypto: {cg_id}")
    return crypto


@router.post("/", response_model=schemas.Crypto)
def create_crypto(crypto_create: schemas.CryptoCreate, db: Session = Depends(get_db)):
    """
    Create a new crypto record based on provided symbol.

    Args:
        crypto_create (schemas.CryptoCreate): Data for the new crypto.
        db (Session): The database session dependency.

    Returns:
        schemas.Crypto: The created crypto object.
    """
    crypto = crypto_service.create_crypto_from_query(db, crypto_create.symbol)
    logger.info(f"Created crypto: {crypto.cg_id}")
    return crypto


@router.put("/{cg_id}", response_model=schemas.Crypto)
def update_crypto(cg_id: str, update_data: schemas.CryptoUpdate, db: Session = Depends(get_db)):
    """
    Update specific fields of an existing crypto.

    Args:
        cg_id (str): The CoinGecko ID of the crypto.
        update_data (schemas.CryptoUpdate): The fields to update.
        db (Session): The database session dependency.

    Returns:
        schemas.Crypto: The updated crypto object.
    """
    updated = crypto_service.update_crypto_fields(db, cg_id, update_data.dict(exclude_unset=True))
    logger.info(f"Updated crypto: {cg_id}")
    return updated


@router.delete("/{cg_id}")
def delete_crypto(cg_id: str, db: Session = Depends(get_db)):
    """
    Delete a crypto record by its CoinGecko ID.

    Args:
        cg_id (str): The CoinGecko ID of the crypto to delete.
        db (Session): The database session dependency.

    Returns:
        dict: A confirmation message.
    """
    crypto_service.delete_crypto(db, cg_id)
    logger.info(f"Deleted crypto: {cg_id}")
    return {"detail": "Deleted"}


@router.post("/update-prices/")
def update_all_prices(db: Session = Depends(get_db)):
    """
    Update the prices for all cryptos stored in the database by fetching data from CoinGecko.

    Args:
        db (Session): The database session dependency.

    Returns:
        dict: A summary of updated cryptos and their new prices.
    """
    cryptos = crypto_service.list_cryptos(db)
    updated = []
    for crypto in cryptos:
        start = time.time()
        data = coingecko.fetch_crypto_data(crypto.cg_id)
        duration = round(time.time() - start, 2)
        logger.info(f"Fetched {crypto.cg_id} in {duration}s")
        if data and data["price"]:
            updated_crypto = crypto_service.update_crypto_price(db, crypto, data["price"])
            updated.append({
                "cg_id": updated_crypto.cg_id,
                "new_price": updated_crypto.price
            })
    logger.info(f"Updated prices for {len(updated)} cryptos")
    return {"updated": updated}
