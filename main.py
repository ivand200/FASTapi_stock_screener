from fastapi import FastAPI, Depends
from typing import List
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import fastapi
from models import DBdj30, DBsp500, DBetf, DBdivs, DBnotes
from schemas import DJ30, SP500, Divs, Etf, Notes
import database

from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi_crudrouter import SQLAlchemyCRUDRouter


router_dj30 = SQLAlchemyCRUDRouter(
    schema = DJ30,
    db_model = DBdj30,
    db = database.get_db
)

router_sp500 = SQLAlchemyCRUDRouter(
    schema = SP500,
    db_model = DBsp500,
    db = database.get_db
)

router_etf = SQLAlchemyCRUDRouter(
    schema = Etf,
    db_model = DBetf,
    db = database.get_db
)


router_divs = SQLAlchemyCRUDRouter(
    schema = Divs,
    db_model = DBdivs,
    db = database.get_db
)


router_notes = SQLAlchemyCRUDRouter(
    schema = Notes,
    db_model = DBnotes,
    db = database.get_db
)


app = FastAPI()
templates = Jinja2Templates("templates")
app.include_router(router_dj30)
app.include_router(router_sp500)
app.include_router(router_etf)
app.include_router(router_divs)
app.include_router(router_notes)

"""Routes"""
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
