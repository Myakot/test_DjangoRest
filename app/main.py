from fastapi import FastAPI

from .wallets import perform_operation, get_balance
from .schemas import OperationRequest

app = FastAPI()

@app.post("/api/v1/wallets/{WALLET_UUID}/operation")
async def perform_operation_endpoint(WALLET_UUID: str, operation: OperationRequest):
    return perform_operation(WALLET_UUID, operation)

@app.get("/api/v1/wallets/{WALLET_UUID}")
async def get_balance_endpoint(WALLET_UUID: str):
    return get_balance(WALLET_UUID)
