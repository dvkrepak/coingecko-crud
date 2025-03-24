import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import SessionLocal
from app.services import coingecko
from app.db import crud

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def update_prices_job():
    logger.info("Scheduled job: Updating crypto prices...")
    db = SessionLocal()
    updated = 0
    try:
        cryptos = crud.get_all_cryptos(db)
        for crypto in cryptos:
            data = coingecko.fetch_crypto_data(crypto.cg_id)
            if data and data["price"]:
                crud.update_crypto_price(db, crypto, data["price"])
                updated += 1
        logger.info(f"Updated prices for {updated} cryptos")
    except Exception as e:
        logger.exception("Error while updating crypto prices", e)
    finally:
        db.close()
