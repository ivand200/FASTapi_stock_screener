from sqlalchemy import Boolean, Column, Float, String, Integer
from sqlalchemy import asc, desc

from database import Base

"""SQLAlchemy models"""
class DBdj30(Base):
    __tablename__ = "dj30"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True)
    name = Column(String, unique=True)
    avg_momentum = Column(Float)
    ep = Column(Float)


class DBsp500(Base):
    __tablename__ = "sp500"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True)
    name = Column(String, unique=True)
    avg_momentum = Column(Float)
    ep = Column(Float)


class DBdivs(Base):
    __tablename__ = "divs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True)
    name = Column(String, unique=True)
    div_p = Column(Float)


class DBetf(Base):
    __tablename__ = "etf"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True)
    name = Column(String, unique=True)
    momentum_12_1 = Column(Float)
    ma10 = Column(Float)


class DBnotes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user = Column(String)
