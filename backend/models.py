from sqlalchemy import Column, Integer, String, DateTime, func, Boolean,JSON
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    role = Column(String, default="user")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    item = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())



class BlockModel(Base):
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    timestamp = Column(DateTime)
    transactions = Column(JSON)
    previous_hash = Column(String)
    hash = Column(String)
    nonce = Column(Integer)  # eklendi


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    only_same_neighborhood = Column(Boolean, default=True)
