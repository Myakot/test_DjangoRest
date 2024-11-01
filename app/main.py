from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .wallets import perform_operation, get_balance
from .schemas import OperationRequest

app = FastAPI()


@app.post("/api/v1/wallets/{WALLET_UUID}/operation")
async def perform_operation_endpoint(WALLET_UUID: str, operation: OperationRequest):
    return perform_operation(WALLET_UUID, operation)


@app.get("/api/v1/wallets/{WALLET_UUID}")
async def get_balance_endpoint(WALLET_UUID: str):
    return get_balance(WALLET_UUID)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Wallet API",
        version="1.0.0",
        description="API documentation for Wallet API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
