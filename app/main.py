from fastapi import FastAPI

from app.core.logging import setup_logging
from app.core.scheduler import update_prices_job, scheduler
from app.core.settings import settings
from app.db.database import engine
from app.db.models import Base
from app.api.routes_crypto import router as crypto_router

setup_logging()
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(crypto_router, prefix="/cryptos", tags=["Cryptos"])


@app.on_event("startup")
def start_scheduler():
    update_prices_job()
    scheduler.add_job(update_prices_job, "interval", minutes=settings.UPDATE_INTERVAL_MINUTES)
    scheduler.start()
