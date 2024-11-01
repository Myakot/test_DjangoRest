import threading

from typing import Dict
from fastapi import HTTPException

from .database import Session
from .models import Wallet
from .schemas import OperationRequest

locks: Dict[str, threading.Lock] = {}


def perform_operation(WALLET_UUID: str, operation: OperationRequest):
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


def get_balance(WALLET_UUID: str):
    session = Session()
    wallet = session.query(Wallet).get(WALLET_UUID)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}
