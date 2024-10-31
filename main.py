import os
import threading

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Wallet
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
app = FastAPI()

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

class OperationRequest(BaseModel):
    operation_type: str
    amount: int

locks = {}

@app.post("/api/v1/wallets/{WALLET_UUID}/operation")
async def perform_operation(WALLET_UUID: str, operation: OperationRequest):
    if WALLET_UUID not in locks:
        locks[WALLET_UUID] = threading.Lock()
    with locks[WALLET_UUID]:
        session = Session()
        try:
            wallet = session.query(Wallet).with_for_update().get(WALLET_UUID)
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet not found")

            if operation.amount < 0:
                raise HTTPException(status_code=400, detail="Invalid amount")

            if operation.operation_type == "DEPOSIT":
                wallet.balance += operation.amount
            elif operation.operation_type == "WITHDRAW":
                if wallet.balance < operation.amount:
                    raise HTTPException(status_code=400, detail="Insufficient funds")
                wallet.balance -= operation.amount
            else:
                raise HTTPException(status_code=400, detail="Invalid operation type")

            session.commit()
            return {"balance": wallet.balance}
        except HTTPException as e:
            session.rollback()
            raise e
        except Exception:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            session.close()

@app.get("/api/v1/wallets/{WALLET_UUID}")
async def get_balance(WALLET_UUID: str):
    session = Session()
    wallet = session.query(Wallet).get(WALLET_UUID)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}
