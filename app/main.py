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

# Set up logging
setup_logging()

# Initialize FastAPI app
app = FastAPI()

# --- Database Setup ---
init_db()  # Initialize the database (create tables)

# --- Mount static files and templates ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")  # Serve static files

# --- Include routers for different API routes ---
app.include_router(ui_router)  # UI-related routes
app.include_router(crypto_router, prefix="/cryptos", tags=["Cryptos"])  # Crypto-related routes


# --- Scheduler Setup ---
@app.on_event("startup")
def start_scheduler():
    """
    Start the scheduler to update cryptocurrency prices at the specified interval.

    Runs the price update job in a separate thread on startup, and schedules it
    to run periodically based on the configuration in settings.
    """
    # Run price updates in a separate thread
    Thread(target=update_prices_job, daemon=True).start()

    # Add the price update job to the scheduler with an interval
    scheduler.add_job(update_prices_job, "interval", minutes=settings.UPDATE_INTERVAL_MINUTES)
    scheduler.start()
