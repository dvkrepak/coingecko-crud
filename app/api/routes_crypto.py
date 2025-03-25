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
    cryptos = crypto_service.list_cryptos(db)
    logger.info(f"Retrieved {len(cryptos)} cryptos")
    return cryptos


@router.get("/{cg_id}", response_model=schemas.Crypto)
def read_crypto(cg_id: str, db: Session = Depends(get_db)):
    crypto = crypto_service.get_crypto_by_id(db, cg_id)
    logger.info(f"Retrieved crypto: {cg_id}")
    return crypto


@router.post("/", response_model=schemas.Crypto)
def create_crypto(crypto_create: schemas.CryptoCreate, db: Session = Depends(get_db)):
    crypto = crypto_service.create_crypto_from_query(db, crypto_create.symbol)
    logger.info(f"Created crypto: {crypto.cg_id}")
    return crypto


@router.put("/{cg_id}", response_model=schemas.Crypto)
def update_crypto(cg_id: str, update_data: schemas.CryptoUpdate, db: Session = Depends(get_db)):
    updated = crypto_service.update_crypto_fields(db, cg_id, update_data.dict(exclude_unset=True))
    logger.info(f"Updated crypto: {cg_id}")
    return updated


@router.delete("/{cg_id}")
def delete_crypto(cg_id: str, db: Session = Depends(get_db)):
    crypto_service.delete_crypto(db, cg_id)
    logger.info(f"Deleted crypto: {cg_id}")
    return {"detail": "Deleted"}


@router.post("/update-prices/")
def update_all_prices(db: Session = Depends(get_db)):
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
