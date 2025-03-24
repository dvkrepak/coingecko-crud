from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app import crud, coingecko

scheduler = BackgroundScheduler()


def update_prices_job():
    db = SessionLocal()
    try:
        cryptos = crud.get_all_cryptos(db)
        for crypto in cryptos:
            data = coingecko.fetch_crypto_data(crypto.cg_id)
            if data and data["price"]:
                crud.update_crypto_price(db, crypto, data["price"])
    finally:
        db.close()
