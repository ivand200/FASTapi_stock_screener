from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List

"""Pydantic schemas"""
class DJ30(BaseModel):
    symbol: str
    name: str
    avg_momentum: float

    class Config:
        orm_mode = True


class SP500(BaseModel):
    symbol: str
    name: str
    avg_momentum: float

    class Config:
        orm_mode = True


class Divs(BaseModel):
    symbol: str
    name: str
    div_p: float

    class Config:
        orm_mode = True


class Etf(BaseModel):
    symbol: str
    name: str
    momentum_12_1: float
    ma10: float

    class Config:
        orm_mode = True


class Notes(BaseModel):
    id: int
    text: str
    user: str

    class Config:
        orm_mode = True
