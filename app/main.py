from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database, coingecko

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/cryptos/", response_model=list[schemas.Crypto])
def read_cryptos(db: Session = Depends(get_db)):
    return crud.get_all_cryptos(db)


@app.get("/cryptos/{cg_id}", response_model=schemas.Crypto)
def read_crypto(cg_id: str, db: Session = Depends(get_db)):
    crypto = crud.get_crypto_by_id(db, cg_id.lower())
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return crypto


@app.post("/cryptos/", response_model=schemas.Crypto)
def create_crypto(crypto_create: schemas.CryptoCreate, db: Session = Depends(get_db)):
    data = coingecko.fetch_crypto_data(crypto_create.symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Symbol not found on Coingecko")

    cg_id = data["id"].lower()
    if crud.get_crypto_by_id(db, cg_id):
        raise HTTPException(status_code=400, detail="Crypto already exists")

    new_crypto = models.Crypto(
        cg_id=cg_id,
        symbol=data["symbol"].lower(),
        name=data["name"],
        price=data["price"]
    )
    return crud.create_crypto(db, new_crypto)


@app.put("/cryptos/{cg_id}", response_model=schemas.Crypto)
def update_crypto(cg_id: str, update_data: schemas.CryptoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_crypto(db, cg_id.lower(), update_data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return updated


@app.delete("/cryptos/{cg_id}", response_model=schemas.Crypto)
def delete_crypto(cg_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_crypto(db, cg_id.lower())
    if not deleted:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return deleted


@app.post("/update-prices/")
def update_all_prices(db: Session = Depends(get_db)):
    cryptos = crud.get_all_cryptos(db)
    updated = []

    for crypto in cryptos:
        data = coingecko.fetch_crypto_data(crypto.cg_id)
        if data and data["price"]:
            updated_crypto = crud.update_crypto_price(db, crypto, data["price"])
            updated.append({
                "cg_id": updated_crypto.cg_id,
                "new_price": updated_crypto.price
            })

    return {"updated": updated}
