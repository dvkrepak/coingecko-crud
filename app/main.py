from threading import Thread

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.logging import setup_logging
from app.core.scheduler import scheduler, update_prices_job
from app.core.settings import settings
from app.db.database import engine, init_db
from app.db.models import Base
from app.api.routes_crypto import router as crypto_router
from app.ui.routes_web import router as ui_router

setup_logging()

app = FastAPI()

# --- Database ---
init_db()

# --- Mount static & templates ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- Routers ---
app.include_router(ui_router)
app.include_router(crypto_router, prefix="/cryptos", tags=["Cryptos"])


# --- Scheduler ---
@app.on_event("startup")
def start_scheduler():
    # Run price updates in a separate thread
    Thread(target=update_prices_job, daemon=True).start()

    scheduler.add_job(update_prices_job, "interval", minutes=settings.UPDATE_INTERVAL_MINUTES)
    scheduler.start()
