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


@app.post("/cryptos/", response_model=schemas.Crypto)
def create_crypto(crypto_create: schemas.CryptoCreate, db: Session = Depends(get_db)):
    # First get the data from Coingecko
    data = coingecko.fetch_crypto_data(crypto_create.symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Symbol not found on Coingecko")

    # Check the symbol from the Coingecko (for example, "btc")
    db_crypto = crud.get_crypto_by_symbol(db, symbol=data["symbol"].lower())
    if db_crypto:
        raise HTTPException(status_code=400, detail="Symbol already exists")

    new_crypto = models.Crypto(
        symbol=data["symbol"].lower(),
        name=data["name"],
        price=data["price"]
    )
    return crud.create_crypto(db, new_crypto)


@app.get("/cryptos/", response_model=list[schemas.Crypto])
def read_cryptos(db: Session = Depends(get_db)):
    return crud.get_all_cryptos(db)
