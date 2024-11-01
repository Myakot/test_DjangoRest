from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(String, primary_key=True)
    balance = Column(Integer, default=0)
