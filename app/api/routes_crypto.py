import logging
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services import coingecko
from app.db import schemas, crud, models

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=list[schemas.Crypto])
def read_cryptos(db: Session = Depends(get_db)):
    cryptos = crud.get_all_cryptos(db)
    logger.info(f"Retrieved {len(cryptos)} cryptos")
    return cryptos


@router.get("/{cg_id}", response_model=schemas.Crypto)
def read_crypto(cg_id: str, db: Session = Depends(get_db)):
    crypto = crud.get_crypto_by_id(db, cg_id.lower())
    if not crypto:
        logger.warning(f"Crypto not found: {cg_id}")
        raise HTTPException(status_code=404, detail="Crypto not found")
    logger.info(f"Retrieved crypto: {cg_id}")
    return crypto


@router.post("/", response_model=schemas.Crypto)
def create_crypto(crypto_create: schemas.CryptoCreate, db: Session = Depends(get_db)):
    data = coingecko.fetch_crypto_data(crypto_create.symbol)
    if not data:
        logger.warning(f"Symbol not found on Coingecko: {crypto_create.symbol}")
        raise HTTPException(status_code=404, detail="Symbol not found on Coingecko")

    cg_id = data["id"].lower()
    if crud.get_crypto_by_id(db, cg_id):
        logger.warning(f"Duplicate crypto create attempt: {cg_id}")
        raise HTTPException(status_code=400, detail="Crypto already exists")

    new_crypto = models.Crypto(
        cg_id=cg_id,
        symbol=data["symbol"].lower(),
        name=data["name"],
        price=data["price"]
    )
    logger.info(f"Created crypto: {cg_id}")
    return crud.create_crypto(db, new_crypto)


@router.put("/{cg_id}", response_model=schemas.Crypto)
def update_crypto(cg_id: str, update_data: schemas.CryptoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_crypto(db, cg_id.lower(), update_data.dict(exclude_unset=True))
    if not updated:
        logger.warning(f"Update failed: crypto not found: {cg_id}")
        raise HTTPException(status_code=404, detail="Crypto not found")
    logger.info(f"Updated crypto: {cg_id}")
    return updated


@router.delete("/{cg_id}", response_model=schemas.Crypto)
def delete_crypto(cg_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_crypto(db, cg_id.lower())
    if not deleted:
        logger.warning(f"Delete failed: crypto not found: {cg_id}")
        raise HTTPException(status_code=404, detail="Crypto not found")
    logger.info(f"Deleted crypto: {cg_id}")
    return deleted


@router.post("/update-prices/")
def update_all_prices(db: Session = Depends(get_db)):
    cryptos = crud.get_all_cryptos(db)
    updated = []
    for crypto in cryptos:
        start = time.time()
        data = coingecko.fetch_crypto_data(crypto.cg_id)
        duration = round(time.time() - start, 2)
        logger.info(f"Fetched {crypto.cg_id} in {duration}s")
        if data and data["price"]:
            updated_crypto = crud.update_crypto_price(db, crypto, data["price"])
            updated.append({
                "cg_id": updated_crypto.cg_id,
                "new_price": updated_crypto.price
            })
    logger.info(f"Updated prices for {len(updated)} cryptos")
    return {"updated": updated}
