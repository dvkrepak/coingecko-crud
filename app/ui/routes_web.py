import logging
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette import status

from app.db.database import get_db
from app.services import crypto_service

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def dashboard(request: Request, q: str = "", db: Session = Depends(get_db)):
    all_cryptos = crypto_service.list_cryptos(db)
    query = q.strip().lower()

    if query:
        cryptos = [
            c for c in all_cryptos
            if query in c.symbol.lower() or query in c.name.lower()
        ]
    else:
        cryptos = all_cryptos

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cryptos": cryptos,
        "q": q
    })


@router.post("/add")
def add_crypto(request: Request, symbol: str = Form(...), db: Session = Depends(get_db)):
    try:
        crypto_service.create_crypto_from_query(db, symbol)
    except HTTPException as e:
        logger.warning(f"Add crypto failed: {e.detail}")

        options = []
        message = None

        if isinstance(e.detail, dict):
            error = e.detail.get("error")
            message = e.detail.get("message")
            options = e.detail.get("options", [])
        else:
            error = e.detail

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "cryptos": crypto_service.list_cryptos(db),
            "error": error,
            "message": message,
            "options": options,
            "q": ""
        }, status_code=e.status_code)

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)



@router.post("/delete/{cg_id}")
def delete_crypto(cg_id: str, db: Session = Depends(get_db)):
    try:
        crypto_service.delete_crypto(db, cg_id)
        logger.info(f"Deleted crypto: {cg_id}")
    except HTTPException as e:
        logger.warning(f"Delete crypto failed: {e.detail}")
    except Exception:
        logger.exception(f"Unexpected error while deleting crypto: {cg_id}")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
